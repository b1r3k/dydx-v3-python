from dydx3.constants import NETWORK_ID_ROPSTEN
from dydx3.helpers.request_helpers import iso_to_epoch_seconds
from dydx3.starkex.transfer import SignableTransfer

MOCK_PUBLIC_KEY = (
    '3b865a18323b8d147a12c556bfb1d502516c325b1477a23ba6c77af31f020fd'
)
MOCK_PRIVATE_KEY = (
    '58c7d5a90b1776bde86ebac077e053ed85b0f7164f53b080304a531947f46e3'
)
MOCK_SIGNATURE = (
    '06b72146028a7f0092557a3a04e9916bd4ae1fba0a4bd92670ef80e2293f7386'
    + '04c0918a7a8e622e463d40f24984c23fd8bab2cd32980676ba666f55c6efeaf3'
)

# Mock transfer params.
TRANSFER_PARAMS = {
    'sender_position_id': 12345,
    'receiver_position_id': 67890,
    'receiver_public_key': (
        '05135ef87716b0faecec3ba672d145a6daad0aa46437c365d490022115aba674'
    ),
    'human_amount': '49.478023',
    'expiration_epoch_seconds': iso_to_epoch_seconds(
        '2020-09-17T04:15:55.028Z',
    ),
    'client_id': (
        'This is an ID that the client came up with to describe this transfer'
    ),
}


class TestTransfer():

    def test_sign_transfer(self):
        transfer = SignableTransfer(
            **TRANSFER_PARAMS, network_id=NETWORK_ID_ROPSTEN)
        signature = transfer.sign(MOCK_PRIVATE_KEY)
        assert signature == MOCK_SIGNATURE

    def test_sign_transfer_different_client_id(self):
        alternative_transfer_params = {**TRANSFER_PARAMS}
        alternative_transfer_params['client_id'] += '!'

        transfer = SignableTransfer(
            **alternative_transfer_params,
            network_id=NETWORK_ID_ROPSTEN
        )
        signature = transfer.sign(MOCK_PRIVATE_KEY)
        assert signature != MOCK_SIGNATURE

    def test_sign_transfer_different_receiver_position_id(self):
        alternative_transfer_params = {**TRANSFER_PARAMS}
        alternative_transfer_params['receiver_position_id'] += 1

        transfer = SignableTransfer(
            **alternative_transfer_params,
            network_id=NETWORK_ID_ROPSTEN
        )
        signature = transfer.sign(MOCK_PRIVATE_KEY)
        assert signature != MOCK_SIGNATURE

    def test_verify_signature(self):
        transfer = SignableTransfer(
            **TRANSFER_PARAMS, network_id=NETWORK_ID_ROPSTEN)
        assert transfer.verify_signature(MOCK_SIGNATURE, MOCK_PUBLIC_KEY)

    def test_starkware_representation(self):
        transfer = SignableTransfer(
            **TRANSFER_PARAMS, network_id=NETWORK_ID_ROPSTEN)
        starkware_transfer = transfer.to_starkware()
        assert starkware_transfer.quantums_amount == 49478023

        # Order expiration should be rounded up and should have a buffer added.
        assert starkware_transfer.expiration_epoch_hours == 444533
