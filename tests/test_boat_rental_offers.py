import pytest

from boat_rental_offers import BoatRentalOffer, InvalidImmatriculationNumberBoat


def test_get_type_boat():
    test_cases = [
        {
            "offer": BoatRentalOffer("123456", True, "dummy_url"),
            "expected": "NUC",
        },
        {
            "offer": BoatRentalOffer("TLA12345", True, "dummy_url"),
            "expected": "NUP",
        },
    ]

    for tc in test_cases:
        result = tc["offer"].get_boat_type()
        assert result == tc["expected"]

    offer = BoatRentalOffer("invalid_immatriculation_number_123", True, "dummy_url")
    with pytest.raises(InvalidImmatriculationNumberBoat):
        offer.get_boat_type()


def test_is_illegal():
    with_skipper = True
    url = "dummy_url"
    offer_nup_illegal = BoatRentalOffer("TLA12345", with_skipper, url)
    expected = True
    result = offer_nup_illegal.is_illegal()
    assert result == expected

    without_skipper = False
    offer_nup_legal = BoatRentalOffer("TLA12345", without_skipper, url)
    expected = False
    result = offer_nup_legal.is_illegal()
    assert result == expected
