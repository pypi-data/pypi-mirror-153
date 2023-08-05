##
# File:     Register.py
# Created:  15-Feb-2017
# Updates:
##
"""
Off-line API registration -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import argparse
import logging

from wwpdb.utils.ws_utils.TokenUtils import JwtTokenUtils

# Create logger
logger = logging.getLogger()
ch = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class Register(object):
    """Off-line API registration -"""

    def __init__(self):
        pass
        #

    def makeAccessToken(
        self,
        emailAddress,
        tokenPrefix="CONTENTWS",
        expireDays=30,
        tokenFileName="onedep_biocuration_apikey.jwt",
    ):
        """Test acquire new or existing token and write to disk"""
        try:
            tU = JwtTokenUtils(tokenPrefix=tokenPrefix)
            tokenId, jwtToken = tU.getToken(emailAddress, expireDays=expireDays)
            logging.info("For e-mail %r token ID %r is %r ", emailAddress, tokenId, jwtToken)
            tD = tU.parseToken(jwtToken)
            logging.info("token %r payload %r ", tokenId, tD)
            #
            with open(tokenFileName, "w") as outfile:
                outfile.write("%s" % jwtToken)
            logging.info("token written to %r ", tokenFileName)
            ok = True
        except Exception as e:
            logging.exception("Making token failed")
            logging.exception(e)
            ok = False
        return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="debugging",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "--emailAddress",
        help="email address",
        type=str,
        default="jdwestbrook@gmail.com",
    )
    parser.add_argument("--tokenPrefix", help="tokenPrefix", type=str, default="CONTENTWS")
    parser.add_argument("--expireDays", help="expireDays", type=int, default=30)

    args = parser.parse_args()
    logger.setLevel(args.loglevel)

    reg = Register()
    reg.makeAccessToken(
        emailAddress=args.emailAddress,
        tokenPrefix=args.tokenPrefix,
        expireDays=args.expireDays,
    )


if __name__ == "__main__":
    main()
