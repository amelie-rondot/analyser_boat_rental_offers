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
