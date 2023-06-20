import pytest

from boat_rental_offers import BoatRentalOffer, InvalidImmatriculationNumberBoat

URL = "dummy_url"
WITH_SKIPPER = True
WITHOUT_SKIPPER = False
NUC_NUMBER = "123456"  # NUC boat immatriculation number
NUP_NUMBER = "TLA12345"  # NUP boat immatriculation number
INVALID_NUMBER = "invalid_number_123"  # invalid boat immatriculation number


def test_get_type_boat():
    test_cases = [
        {
            "offer": BoatRentalOffer(NUC_NUMBER, WITH_SKIPPER, URL),
            "expected": "NUC",
        },
        {
            "offer": BoatRentalOffer(NUP_NUMBER, WITH_SKIPPER, URL),
            "expected": "NUP",
        },
    ]

    for tc in test_cases:
        result = tc["offer"].get_boat_type()
        assert result == tc["expected"]

    offer = BoatRentalOffer(INVALID_NUMBER, WITH_SKIPPER, URL)
    with pytest.raises(InvalidImmatriculationNumberBoat):
        offer.get_boat_type()


def test_is_illegal():

    # Test case: the boat is a NUP, and it is rented with a skipper -> illegal offer
    offer_nup_illegal = BoatRentalOffer(NUP_NUMBER, WITH_SKIPPER, URL)
    expected = True
    result = offer_nup_illegal.is_illegal()
    assert result == expected

    without_skipper = False
    # Test case: the boat is a NUP, and it is rented without a skipper -> legal offer
    offer_nup_legal = BoatRentalOffer(NUP_NUMBER, without_skipper, URL)
    expected = False
    result = offer_nup_legal.is_illegal()
    assert result == expected

    # Test case: the boat is a NUC, and it is rented without a skipper -> illegal offer
    offer_nuc_illegal = BoatRentalOffer(NUC_NUMBER, without_skipper, URL)
    expected = True
    result = offer_nuc_illegal.is_illegal()
    assert result == expected

    # Test case: the boat is a NUC, and it is rented with a skipper -> legal offer
    offer_nup_legal = BoatRentalOffer(NUC_NUMBER, WITH_SKIPPER, URL)
    expected = False
    result = offer_nup_legal.is_illegal()
    assert result == expected
