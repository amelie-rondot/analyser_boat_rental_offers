from boat_rental_offers import BoatRentalOffer


def test_get_type_boat():
    offer_nuc = BoatRentalOffer("123456", True, "dummy_url")
    expected_boat_type = "NUC"
    result = offer_nuc.get_type_boat()
    assert result == expected_boat_type


