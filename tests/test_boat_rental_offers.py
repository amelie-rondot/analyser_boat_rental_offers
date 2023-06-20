import pytest

from boat_rental_offers import BoatRentalOffer, InvalidImmatriculationNumberBoat


def test_get_type_boat():
    offer_nuc = BoatRentalOffer("123456", True, "dummy_url")
    expected_boat_type = "NUC"
    result = offer_nuc.get_type_boat()
    assert result == expected_boat_type

    offer_nup = BoatRentalOffer("TLA12345", True, "dummy_url")
    expected_boat_type = "NUP"
    result = offer_nup.get_type_boat()
    assert result == expected_boat_type

    unvalid_immat_number_offer = BoatRentalOffer("invalid_immatriculation_number_123", True, "dummy_url")
    with pytest.raises(InvalidImmatriculationNumberBoat):
        unvalid_immat_number_offer.get_type_boat()
