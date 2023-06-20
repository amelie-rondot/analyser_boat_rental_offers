import pytest

from boat_rental_offers import BoatRentalOffer, InvalidImmatriculationNumberBoat

URL = "dummy_url"
WITH_SKIPPER = True
WITHOUT_SKIPPER = False
NUC_NUMBER = "123456"  # NUC boat immatriculation number
NUP_NUMBER = "TLA12345"  # NUP boat immatriculation number
INVALID_NUMBER = "invalid_number_123"  # invalid boat immatriculation number


def test_boat_rental_offer_constructor():
    # Test cases:
    # - Check that self.boat_immatriculation_number is a str
    # - Check that self.with_skipper is a boolean
    # - Check that self.url is a str
    pass


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

    test_cases = [
        {
            # Illegal offer: the boat is a NUP, and it is rented with a skipper
            "offer": BoatRentalOffer(NUP_NUMBER, WITH_SKIPPER, URL),
            "expected": True,
        },
        {
            # Legal offer: The boat is a NUP, and it is rented without a skipper
            "offer": BoatRentalOffer(NUP_NUMBER, WITHOUT_SKIPPER, URL),
            "expected": False,
        },
        {
            # Illegal offer: The boat is a NUC, and it is rented without a skipper
            "offer": BoatRentalOffer(NUC_NUMBER, WITHOUT_SKIPPER, URL),
            "expected": True,
        },
        {
            # Legal offer: The boat is a NUC, and it is rented with a skipper
            "offer": BoatRentalOffer(NUC_NUMBER, WITH_SKIPPER, URL),
            "expected": False,
        },
    ]

    for tc in test_cases:
        result = tc["offer"].is_illegal()
        assert result == tc["expected"]

