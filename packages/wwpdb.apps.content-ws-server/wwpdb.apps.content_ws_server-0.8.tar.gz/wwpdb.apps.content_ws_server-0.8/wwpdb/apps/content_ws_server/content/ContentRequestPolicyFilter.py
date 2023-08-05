##
# File:  ContentRequestPolicyFilter.py
# Date:  05-Jul-2017  E. Peisach
#
# Update:
##
"""
Policy filtering of content request for web service -

"""
__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import logging

#
logger = logging.getLogger()


class ContentRequestPolicyFilter(object):
    """
    Manage various policy filters for entry data. A post request filter.

    """

    def __init__(self):

        pass

    def filterContent(self, contentType, rD):
        """Filters rD based on contentType.  Returns new content or {} if all removed"""

        if not rD:
            return rD

        logger.debug("Content in %r", rD)
        if "sasbdb" in contentType:
            # Policy 1: suppress title and author
            pDS = rD.get("pdbx_database_status", None)
            if pDS:
                logger.debug("Filtering %r", pDS)
                tS = pDS[0].get("title_suppression", None)
                if tS and tS in ["Y"]:
                    logger.debug("Removing author and title and contact")
                    rD["audit_author"] = [{}]
                    rD["pdbx_contact_author"] = [{}]
                    rD["struct"][0]["title"] = ""
            # Policy 2: If not sas - you get nothing
            removeAll = True
            pDSF = rD.get("pdbx_depui_status_flags", None)
            if pDSF:
                hSD = pDSF[0].get("has_sas_data", None)
                if hSD and hSD in ["Y"]:
                    removeAll = False
            if removeAll:
                rD = {}

        logger.debug("Content out %r", rD)

        return rD
