import enum
import re


class BoatType(enum.Enum):
    """
    Defines the type of boat, which could be:
        - NUP meaning "Navire à Usage Personnel" in French
        - NUC meaning "Navire à Usage Commercial" in French
    """
    NUP = "NUP"
    NUC = "NUC"


class InvalidImmatriculationNumberBoat(Exception):
    """
    An `InvalidImmatriculationNumberBoat` exception is used when the boat immatriculation
    number does not correspond to a French codified immatriculation numbers formats for boat:
    see get_boat_type method for details.
    """
    def __init__(self, message):
        super().__init__(message)


class BoatRentalOffer:
    """
    A BoatRentalOffer is used to implements a boat rental offer.
    It is defined by:
     - the immatriculation number of the boat related to the rental offer
     - the fact that the boat related to the rental offer is rented with a skipper or not
     - the url of the rental offer
    """

    def __init__(self, boat_immatriculation_number: str, with_skipper: bool, offer_url: str):
        """
        :param boat_immatriculation_number: str: the immatriculation number of the boat related to the rental offer
        :param with_skipper: bool: set to True if the offer offers to rent the boat with a skipper, set to False if not
        :param offer_url: str: url of the offer
        """
        self.boat_immatriculation_number = boat_immatriculation_number
        self.with_skipper = with_skipper
        self.offer_url = offer_url

    def get_boat_type(self) -> BoatType:
        """
        Get the boat type (NUC "Navire à Usage Commercial" in French or
        NUP "Navire à Usage Personnel") according to the `boat_immatriculation_number`.

        The French boats have two codified immatriculation numbers formats:
        - either a series of 5 or 6 numbers, used for NUC boats, for example "104641"
        - either a series of 3 letters followed by 5 numbers, used for NUP boats, for example "TLF70259"

        :return: BoatType
        """

        rex_nuc = re.compile("^[0-9]{5,6}$")
        rex_nup = re.compile("^[a-zA-Z]{3}[0-9]{5}$")
        if rex_nuc.match(self.boat_immatriculation_number):
            return "NUC"
        elif rex_nup.match(self.boat_immatriculation_number):
            return "NUP"
        else:
            raise InvalidImmatriculationNumberBoat("Le numéro d'immatriculation du bateau ne correspond ni "
                                                   "à un numéro d'immatriculation de NUC ni de NUP.")

    def is_illegal(self):
        """
        Defines if the boat rental offer is illegal according to the type of the boat related to the offer
        and if the boat is rented with a skipper:
        An offer is considered as illegal in these cases:
        - the boat is a NUP, and it is rented with a skipper (most of the cases of illegal offers)
        - the boat is a NUC, and it is rented without a skipper
        At the contrary, an offer is considered as legal in these cases:
        - the boat is a NUP, and it is rented without a skipper (most of the cases of legal offers)
        - the boat is a NUC, and it is rented with a skipper

        :return: bool
        """
        if self.get_boat_type() == "NUP" and self.with_skipper:
            return True
        elif self.get_boat_type() == "NUP" and not self.with_skipper:
            return False
        # Test case: the boat is a NUC, and it is rented without a skipper -> illegal offer
        elif self.get_boat_type() == "NUC" and not self.with_skipper:
            return False
