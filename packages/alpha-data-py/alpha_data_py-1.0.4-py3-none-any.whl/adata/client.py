import base64
import time

import grpc
import registry_pb2
import registry_pb2_grpc
from tickstore import client
from tickstore.query import QuerySettings

from adata.iterators import FloatIterator, LiquidityIterator, OHLCVIterator, TradeIterator
from .consts import FREQUENCIES, ports, DATA_CLIENT_LIVE, DATA_CLIENT_1S, DATA_CLIENT_1M, DATA_CLIENT_1H


def check_frequency(frequency):
    return frequency in FREQUENCIES


class Client:
    def __init__(self, api_key, api_secret):
        self.__api_key = api_key
        self.__api_secret = api_secret
        license_id_bytes = base64.b64decode(api_key)
        license_id = int.from_bytes(license_id_bytes, "little")
        registry_address = "registry.alphaticks.io:8001"
        channel = grpc.insecure_channel(registry_address)
        self.__stub = registry_pb2_grpc.PublicRegistryStub(channel)
        interceptors = [
            Interceptor(license_id, api_secret)
        ]
        self.__stores = {
            DATA_CLIENT_LIVE: client.Client("store.alphaticks.io:" + ports[DATA_CLIENT_LIVE], interceptors),
            DATA_CLIENT_1S: client.Client("store.alphaticks.io:" + ports[DATA_CLIENT_1S], interceptors),
            DATA_CLIENT_1M: client.Client("store.alphaticks.io:" + ports[DATA_CLIENT_1M], interceptors),
            DATA_CLIENT_1H: client.Client("store.alphaticks.io:" + ports[DATA_CLIENT_1H], interceptors),
        }

    def get_securities(self):
        request = registry_pb2.SecuritiesRequest()
        res = self.__stub.Securities(request)
        return res.securities

    def get_assets(self):
        request = registry_pb2.AssetsRequest()
        res = self.__stub.Assets(request)
        return res.assets

    def stream_trade_price(self, sec, batch_size=1000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_LIVE)
        now = round(time.time_ns() / 1000000)
        qs = QuerySettings(
            streaming=True,
            batch_size=batch_size,
            timeout=100000,
            selector='SELECT TradePrice(trade) WHERE ID="{0}"'.format(sec.security_id),
            frm=now,
            to=now * 10,
            object_type="Float64"
        )
        q = c.new_query(qs)
        return FloatIterator(q)

    def stream_funding_rate(self, sec, batch_size=1000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_1H)
        now = round(time.time_ns() / 1000000)
        qs = QuerySettings(
            streaming=True,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT funding WHERE ID="{0}"'.format(sec.security_id),
            frm=now,
            to=now * 10,
            object_type="Float64"
        )
        q = c.new_query(qs)
        return FloatIterator(q)

    def stream_liquidation(self, sec, batch_size=1000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_1M)
        now = round(time.time_ns() / 1000000)
        qs = QuerySettings(
            streaming=True,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT NewLiquidation(liquidation) WHERE ID="{0}"'.format(sec.security_id),
            frm=now,
            to=now * 10,
        )
        q = c.new_query(qs)
        return TradeIterator(q)

    def stream_trade(self, sec, batch_size=1000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_LIVE)
        now = round(time.time_ns() / 1000000)
        qs = QuerySettings(
            streaming=True,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT Trade(trade) WHERE ID="{0}"'.format(sec.security_id),
            frm=now,
            to=now * 10,
        )
        q = c.new_query(qs)
        return TradeIterator(q)

    def stream_open_interest(self, sec, batch_size=1000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_1M)
        now = round(time.time_ns() / 1000000)
        qs = QuerySettings(
            streaming=True,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT openinterest WHERE ID="{0}"'.format(sec.security_id),
            object_type="Float64",
            frm=now,
            to=now * 10,
        )
        q = c.new_query(qs)
        return FloatIterator(q)

    def stream_ohlcv(self, sec, freq, batch_size=1000, timeout=100000):
        if not check_frequency(freq):
            raise ValueError("frequency value error")
        c = self.__get_store(freq)
        now = round(time.time_ns() / 1000000)
        qs = QuerySettings(
            streaming=True,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT AggOHLCV(ohlcv, "{0}") WHERE ID="{1}" GROUPBY base'.format(freq, sec.security_id),
            frm=now,
            to=now * 10,
        )
        q = c.new_query(qs)
        return OHLCVIterator(q)

    def stream_liquidity(self, sec, freq, depth, batch_size=10000, timeout=100000):
        if not check_frequency(freq):
            raise ValueError("frequency value error")
        if freq < DATA_CLIENT_1M:
            raise ValueError("minimum frequency 1m")
        c = self.__get_store(freq)
        now = round(time.time_ns() / 1000000)
        selector = 'SELECT AggOBLiquidity(obliquidity, "{0}", "{1}", "1000") WHERE ID="{2}" GROUPBY base'\
                       .format(freq, depth, sec.security_id)
        qs = QuerySettings(
            streaming=True,
            batch_size=batch_size,
            timeout=timeout,
            selector=selector,
            frm=now,
            to=now * 10,
        )
        q = c.new_query(qs)
        return LiquidityIterator(q)

    def get_historical_trade_price(self, sec, frm, to, batch_size=10000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_LIVE)
        qs = QuerySettings(
            streaming=False,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT TradePrice(trade) WHERE ID="{0}"'.format(sec.security_id),
            frm=int(frm.timestamp() * 1000),
            to=int(to.timestamp() * 1000),
            object_type="Float64"
        )
        q = c.new_query(qs)
        return FloatIterator(q)

    def get_historical_funding_rate(self, sec, frm, to, batch_size=10000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_1H)
        qs = QuerySettings(
            streaming=False,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT funding WHERE ID="{0}"'.format(sec.security_id),
            frm=int(frm.timestamp() * 1000),
            to=int(to.timestamp() * 1000),
            object_type="Float64"
        )
        q = c.new_query(qs)
        return FloatIterator(q)

    def get_historical_liquidation(self, sec, frm, to, batch_size=10000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_1M)
        qs = QuerySettings(
            streaming=False,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT NewLiquidation(liquidation) WHERE ID="{0}"'.format(sec.security_id),
            frm=int(frm.timestamp() * 1000),
            to=int(to.timestamp() * 1000),
        )
        q = c.new_query(qs)
        return TradeIterator(q)

    def get_historical_trade(self, sec, frm, to, batch_size=10000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_LIVE)
        qs = QuerySettings(
            streaming=False,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT Trade(trade) WHERE ID="{0}"'.format(sec.security_id),
            frm=int(frm.timestamp() * 1000),
            to=int(to.timestamp() * 1000),
        )
        q = c.new_query(qs)
        return TradeIterator(q)

    def get_historical_open_interest(self, sec, frm, to, batch_size=10000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_1M)
        qs = QuerySettings(
            streaming=False,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT openinterest WHERE ID="{0}"'.format(sec.security_id),
            object_type="Float64",
            frm=int(frm.timestamp() * 1000),
            to=int(to.timestamp() * 1000),
        )
        q = c.new_query(qs)
        return FloatIterator(q)

    def get_historical_ohlcv(self, sec, freq, frm, to, batch_size=10000, timeout=100000):
        if not check_frequency(freq):
            raise ValueError("frequency value error")
        c = self.__get_store(freq)
        qs = QuerySettings(
            streaming=False,
            batch_size=batch_size,
            timeout=timeout,
            selector='SELECT AggOHLCV(ohlcv, "{0}") WHERE ID="{1}" GROUPBY base'.format(freq, sec.security_id),
            frm=int(frm.timestamp() * 1000),
            to=int(to.timestamp() * 1000),
        )
        q = c.new_query(qs)
        return OHLCVIterator(q)

    def get_historical_liquidity(self, sec, freq, depth, frm, to, batch_size=10000, timeout=100000):
        c = self.__get_store(DATA_CLIENT_1M)
        selector = 'SELECT AggOBLiquidity(obliquidity, "{0}", "{1}", "1000") WHERE ID="{2}" GROUPBY base'\
            .format(freq, depth, sec.security_id)
        qs = QuerySettings(
            streaming=False,
            batch_size=batch_size,
            timeout=timeout,
            selector=selector,
            frm=int(frm.timestamp() * 1000),
            to=int(to.timestamp() * 1000),
        )
        q = c.new_query(qs)
        return LiquidityIterator(q)

    def __get_store(self, freq):
        min_score = DATA_CLIENT_1H
        cfreq = 0
        for k in self.__stores:
            if k <= freq:
                score = freq - k
                if score < min_score:
                    min_score = score
                    cfreq = k

        return self.__stores[cfreq]


class Interceptor(grpc.UnaryUnaryClientInterceptor, grpc.UnaryStreamClientInterceptor,
                  grpc.StreamStreamClientInterceptor):
    def __init__(self, license_id, license_key):
        self.license_id = license_id
        self.license_key = license_key

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return continuation(self.__intercept(client_call_details), request)

    def intercept_unary_stream(self, continuation, client_call_details, request):
        return continuation(self.__intercept(client_call_details), request)

    def intercept_stream_stream(self, continuation, client_call_details, request):
        return continuation(self.__intercept(client_call_details), request)

    def __intercept(self, client_call_details):
        base = client_call_details.metadata if client_call_details.metadata is not None else []
        md = base + [("license-id", str(self.license_id))] + [("license-key", self.license_key)]
        new_details = grpc.ClientCallDetails()
        new_details.method = client_call_details.method
        new_details.timeout = client_call_details.timeout
        new_details.metadata = md
        new_details.credentials = client_call_details.credentials
        new_details.wait_for_ready = client_call_details.wait_for_ready
        new_details.compression = client_call_details.compression
        return new_details
