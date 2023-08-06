##
# File:    ConfigInfoData.py
# Date:    28-Mar-2010
#
# Updates:
# 21-Apr-2010 jdw add content types for sequence data.
# 22-Apr-2010 jdw add site specific database server configuration items.
# 27-Apr-2010 jdw allow site id to be set in the constructor.
# 10-Sep-2010 jdw add support for chemical component linkages and assignments.
#                 add directories for chemical component applications and support files.
# 13-Dec-2010 jdw add additional configuration environment for cc-tools apps
# 13-Jan-2011 rps added config entry for 'chem-comp-assign-details' content type
#
# 28-Jun-2011 jdw add CVS chemical components path --
#                 resolve conflicts in PDBe config
#
# 29-Jun-2011 jdw no configuration is set if siteId not provided.
# 21-Sep-2011 rps 'SITE_WEB_APPS_TOP_PATH' key added so that value is driven by siteId
#  2-Apr-2012 jdw add WWPDB_DEV_TEST environment.
#                 add 'SITE_CC_SCRIPT_PATH'
# 10-Apr-2012 jdw add content types for assembly and site annotation
# 14-Jun-2012 jdw add content types for chemical component user selection -
# 08-May-2012 rps Propagated use of 'SITE_CC_SCRIPT_PATH' to config dictionary used for "PDBE" site ID
#                  Added config dictionary for "WWPDB_DEPLOY" site ID
# 11-Jun-2012 rps Added config entry for 'chem-comp-select' content type
#  3-Jul-2012 jdw temporary placeholders added for  'SITE_TOOLS_PATH' and  'SITE_ANNOT_TOOLS_PATH'
# 03-Jul-2012 rps Removed config entry for 'chem-comp-select' content type
#                 and added config entry for 'chem-comp-assign-final' content type.
#                 Modified 'SITE_CC_APPS_PATH' to '/apps/cc-tools-v2' for _wwpdbdeployD
#  7-Jul-2012 jdw add placeholder config entries for annotation modules for PDBe.
# 17-Jul-2012 rps added config dictionary for "WWPDB_SHARE" site ID.
# 25-Jul-2012 rps added keys for 'SITE_MSG_DB_USER_ID' and 'SITE_MSG_DB_USER_PWD'
# 14-Aug-2012 rps added keys for 'SITE_TOOLS_PATH','SITE_PISA_TOP_PATH', 'SITE_ANNOT_TOOLS_PATH',
#                    and 'SITE_SPACE_GROUP_FILE_PATH' to wwpdbdevD dictionary
# 15-Aug-2012 jdw added file type assembly-assign type txt.
# 16-Aug-2012 rps added 'SITE_CIF_EDITOR_URL' key and corresponding values where deemed relevant.
# 28-Aug-2012 rps added 'SITE_ANN_TASKS_URL' key and corresponding values where deemed relevant.
# 30-Aug-2012 rps added 'SITE_CIF_EDITOR_UI_CONFIG_FILE_PATH' key and corresponding values where deemed relevant.
# 04-Sep-2012 rps added 'SITE_MMCIF_DICT_FILE_PATH' key and corresponding values where deemed relevant.
# 05-Sep-2012 jdw added 'SITE_DEPLOY_PATH' to WWPDB_DEPLOY_TEST' configuration seciton.
# 06-Sep-2012 jdw added new file types for topology, validation report and validation data files
# 10-Sep-2012 rps added settings used by mmcif editor to _wwpdbdeployTestD dictionary.
# 17-Sep-2012 rps URLs used for launch of annotation modules now use relative URL form
#                 (RESTORED THIS CHANGE WHICH WAS INADVERTENTLY OVERWRITTEN BY COMMIT SUBMITTED BY SOMEONE ELSE).
# 01-Oct-2012 rps 'SITE_MMCIF_DICT_FILE_PATH' used by WWPDB_DEPLOY and WWPDB_DEPLOY_TEST now points to new 'mmcif_pdbx_v5_next.dic'
# 08-Oct-2012 rps Removed all config dictionaries known to be obsolete (_wwpdbdevTestD, _wwpdbshareD, _rcsbD).
#                    Also added 'SITE_WEB_APPS_SESSIONS_PATH' key/value pairs.
# 10-Oct-2012 rps 'SITE_WEB_APPS_TOP_SESSIONS_PATH' added simply as measure for "backwards-compatibility".
#                    Need to comprehensively determine whether code in various modules actually need to know this value.
#                    May be that this is a legacy item that can be removed if obsolete.
# 18-Oct-2012 jdw  Add configuration for PRD, PRDCC adn FAMILY CVS sandboxes to deployment configuration sections
# 12-Nov-2012 rps Added 'SITE_WEB_APPS_TOP_SESSIONS_PATH' setting for PDBE site ID/_pdbeD dictionary.
# 10-Dec-2012 jdw  Add library path for OpenBabel for CC tools --
# 12-Dec-2012 jdw  Update OpenBabel library version
# 24-Jan-2013 jdw  Add configuration for reference data to DEPLOY and DEPLOY_TEST
# 21-Feb-2013 rps  Add content type configuration for "chem-comp-depositor-info" file
# 23-Feb-2013 jdw  Add taxonomy reference path
# 26-Feb-2013 jdw  Add 'blast-match' file type
# 02-Mar-2013 jdw  Suppress the redundant error message related to site_id.
# 02-Mar-2013 jdw  Require format types in _configTypeInfoD have unique file extensions.
# 04-Apr-2013 jdw  Add map file types.
# 15-Apr-2013 jdw  Add fasta file type
# 16-Apr-2013 jdw  add path to reference sequence databases -  'SITE_REFDATA_SEQUENCE_DB_PATH'
# 18-Apr-2013 jdw  add temporary path variable 'SITE_TMP_DIR'
# 23-Apr-2013 jdw  add SITE_REFDATA_CHEM_COMP_INDEX_PATH
#  1-May-2013 jdw  add 'SITE_PDBX_DICT_NAME'
# 21-May-2013 jdw  add 'SITE_DEPOSIT_STORAGE_PATH'
# 24-Jun-2013 jdw  add site id WWPDB_DEPLOY_INTERNAL for internal production configuration.
# 26-Jun-2013 jdw  add format-check-report file type
# 15-Jul-2013 jdw  add PDBX_V4_DICT_NAME
#  3-Aug-2013 jdw  refactor and simplify, add mac and centos 6 config sections.
#  7-Aug-2013 jdw  add content types for message files and note files --
# 15-Aug-2013 jdw  add content type for sf-convert-diag files
# 09-Sep-2013 rps  add SITE_MSGING_URL key
# 20-Sep-2013 jdw  add site id specific for the public validation server  "WWPDB_DEPLOY_VALSRV_RU"
# 14-Oct-2013 jdw  update content milestone variants -- content type 'correspondence-to-depositor'
# 18-Oct-2013 jdw  update ccpn types
# 24-Dec-2013 jdw  add content type assembly-model-xyz
# 29-Dec-2013 jdw  add 'geometry-check-report' and 'dict-check-report-r4'
# 20-Jan-2014 jdw  add site Id "WWPDB_DEPLOY_PRODUCTION_RU" for production deposition/annotation
# 24-Jan-2014 jdw  add content types for the full pdf report and quality slider images.
# 30-Jan-2014 jdw  add content formats for nmr-restraints and new content-type for nmr peak lists
# 10-Feb-2014 jdw  add mapfix-report
# 20-Feb-2014 jdw  add milestone content type 'upload-convert'
# 22-Feb-2014 jdw  add em2em-report
# 05-Mar-2014 jdw  add 'special-position-report'
# 06-Mar-2014 rps  add 'SITE_DEPOSIT_UI_HOST_NAME'
# 06-Mar-2014 jdw  add PDBJ SITE IDS
# 16-Mar-2014 jdw  update annotation tasks to V2
# 16-Mar-2014 jdw  add separate validation task url at V2
# 19-Mar-2014 jdw  add 'SITE_SERVICE_URL_PATH_PREFIX'
# 25-Mar-2014 rps  add 'SITE_ARCHIVE_NOTIF_EMAILS' as switch for determining whether to archive no-reply comms per site
# 19-Apr-2014 jdw  add 'polymer-linkage-report'
# 26-Apr-2014 jdw  add 'tif' format type
# 28-Apr-2014 rps  add 'gz' format type to _fileFormatExtensionD
#  2-Jun-2014 jdw  add map-header-data type -
# 11-Jun-2014 jdw  add type 'merge-xyz-report'
# 20-Jun-2014 jdw  add content type em-mask
# 24-Jun-2014 jdw  add SITE_PISA_CONF_PATH
#  5-Jul-2014 jdw  add CONTENT_MILESTONE_LIST
#  7-Jul-2014 jdw  add status-history content type
# 14-Jul-2014 jdw  add configuration for da_internal database.  ++
# 16-Jul-2014 jdw  add content types for omit maps
# 24-Jul-2014 jdw  add content type for semi-structured chemical shift files -  'nmr-chemical-shifts-raw'     :  (['nmr-star'],'cs-raw'),
# 31-Jul-2014 jdw  add deposition configuration details
# 22-Aug-2104 jdw  update database locations --
# 23-Aug-2014 jdw  add 'deposit-volume-params'
# 04-Sep-2014 rps  add 'SITE_CIF_EDITOR_UI_CONFIG_FILE_PATH_EM' and 'SITE_CIF_EDITOR_UI_CONFIG_FILE_PATH_NMR'
# 08-Sep-2014 jdw  add  author provided chemical shifts -- 'nmr-chemical-shifts-auth'    :  (['nmr-star','pdbx'],'cs-auth')
# 09-Sep-2014 jdw  add site WWPDB_DEPLOY_ALPHA
# 10-Sep-2014 jdw  set staging database server host to pdb-f-linux-5.rutgers.edu at Rutgers
# 12-Sep-2014 jdw  add  'nmr-chemical-shifts-upload-report' &  'nmr-chemical-shifts-atom-name-report'
# 29-Jan-2015 rps  add 'SITE_DEPOSIT_UI_HOST_NAME': 'wwpdb-deposit-alpha.wwpdb.org' for site WWPDB_DEPLOY_ALPHA
# 30-Jan-2015 jdw  add  format-type mr for nmr-restraints -
# 06-Mar-2015 rps  add  'mdl' format type. Also added SITE_DEPOSIT_UI_HOST_NAME for staging, internal test, and test environments
# 10-Mar-2015 jdw  add  WWPDB_DEPLOY_PRODUCTION_UCSD
# 24-Mar-2015 jdw  update  WWPDB_DEPLOY_PRODUCTION_UCSD for chemical reference data
#  9-Apr-2015 jdw  update  Standardize the path in the source tree to workflow definitions (e.g. wf_engine/wf-defs)
# 11-Apr-2015 jdw  corrections to config host names -
# 13-May-2015 esg  added a few extra file types for EM
# 30-Jun-2015 jdw  add model-emd content type for model data conforming to emd dictionary extensions.
# 20-Jul-2015 jdw  add content type em-volume-header
# 20-Jul-2015 jdw  add content type nmr-nef
# 20-Jul-2015 jdw  add 'SITE_EXT_DICT_MAP_EMD_FILE_PATH'
#  4-Aug-2015 jdw  add types 'nmr-cs-path-list' and 'nmr-cs-auth-file-name-list'
# 15-Aug-2015 jdw  add 'em-half-volume' for half maps -
# 31-Aug-2015 jdw  add cmd-line-args
# 11-Sep-2015 jdw  add WWPDB_DEPLOY_STAGING_RU  WWPDB_DEPLOY_RU
#  2-Oct-2015 jdw  add workflow configuration files  'em-volume-wfcfg' 'em-mask-volume-wfcfg' 'em-additional-volume-wfcfg' 'em-half-volume-wfcfg'
# 16-Oct-2015 jdw  refine beta configuration
# 31-Oct-2015 jdw  add WWPDB_DEPLOY_DEVEL_ALPHA_RU and WWPDB_DEPLOY_DEVEL_PROD_RU - revised config
# 12-Nov-2015 jdw  update OSX configuration
# 13-Nov-2015 jdw  Revise DEVEL config
# 13-Nov-2015 jdw  Revise DEVEL_ALPHA config
# 24-Nov-2015 jdw  correct URL configs for devel nodes
# 04-Dec-2015 jdw  add SITE_LEGACY_DEP_URL
# 07-Dec-2015 jdw  fixed problem with _configSiteMachineName
# 08-Dec-2015 jdw  add SITE_CURRENT_DEP_URL
# 09-Dec-2015 jdw  simplify DEVEL configuration - add config to support WFE in compatibility mode
# 10-Dec-2015 jdw  add WWPDB_DEPLOY_DEVEL2_* configurations additional compatibility tests
# 10-Dec-2015 lm   add FTP_HOST_NAME, FTP_USER_FILE, FTP_DB_FILE, FTP_STORAGE_PATH
# 22-Dec-2015 jdw  update EMAIL config for ALPHA test host
# 26-Dec-2015 jdw  update RCSB/UCSD/PDBj configs for v152-compat release
# 26-Dec-2015 jdw  added WWPDB_DEPLOY_NEXT_RU
# 15-Jan-2016 jdw  update config for DEVEL1 testing -
# 19-Jan-2016 jdw  update ftp configs for remote sites
# 26-Jan-2016 lm   added SITE_UPLOADS_PATH
# 29-Jan-2016 jdw  add configuration changes for production rollout -
#  2-Feb-2016 jdw  update config or devel1 platform to test migration issues
# 18-Feb-2016 jdw  update _TEST_RU server tool path
#  3-Mar-2016 jdw  add port configuration parameters
# 10-Mar-2016 jdw  reset test database name
# 15-Mar-2016 rps  'SITE_INSTANCE_DB_USER_NAME' and 'SITE_INSTANCE_DB_PASSWORD' added
# 19-Mar-2016 jdw  capture site specific parameters and replacements
# 05-Apr-2016 lm   add FTP_PORT_NUMBER, FTP_CONNECT_DETAILS
# 06-Apr-2016 jdw  update cache handling and cleanup unused and duplicated code -
# 06-Apr-2016 jdw  add SITE_DATASET_ID_ASSIGNMENT_DICTIONARY and _siteDataSetIdAssignmentD
# 06-Apr-2016 jdw  add fallback placeholder options for 'SITE_REFDATA_DB_USER_NAME','SITE_REFDATA_DB_PASSWORD',
#                  'SITE_DA_INTERNAL_DB_USER_NAME','SITE_DA_INTERNAL_DB_USER_PASSWORD',
#                  'SITE_MESSAGE_SERVER_HOST_NAME', 'SITE_MESSAGE_ARCHIVE_URL', and 'SITE_MESSAGE_FORWARD_URL'.
# 07-Apr-2016 jdw  added PROJECT_DEPOSIT_SERVICE_DICTIONARY, SITE_ACCESS_INFO_FILE_PATH and SITE_DATASET_SITELOC_FILE_PATH
# 26-Apr-2016 jdw  update fallback resources
#  4-May-2016 jdw  update config for DEVEL2_RU
# 17-May-2016 jdw  add _projectCorrespondSiteServiceD
#  1-Jun-2016 jdw  add _projectForwardingSiteServiceD
#                  add fallback option keys - 'SITE_DA_INTERNAL_DB_RO_USER_NAME' and 'SITE_DA_INTERNAL_DB_RO_PASSWORD'
# 27-Jun-2016 rps  adding 'tiff' to list of acceptable file formats for 'component-image' files uploaded by depositors.
# 12-Jul-2016 jdw  add default id ranges for 'WWPDB_DEPLOY_VALSRV2_RU'
# 15-Jul-2016 jdw  update correspondence endpoints for 'WWPDB_DEPLOY_DEPGRP1/2_RU
# 26-Jul-2016 ep   Separate default ranges for WWPDB_DEPLOY_TEST_RU and WWPDB_DEPLOY_ALPHA_RU. Update range for 'WWPDB_DEPLOY_VALSRV2_RU'
# 08-Aug-2016 jdw  add WWPDB_DEPLOY_LEGACY_RU and id range for this site -
# 16-Aug-2016 jdw  add 'WWPDB_DEPLOY_PRODUCTION_BACKUP_RU' id range
# 13-Sep-2016 ep   add 'WWPDB_DEPLOY_LCLTEST_RU' id range
# 19-Sep-2016 ep   add 'WWPDB_DEPLOY_LEGACY_RU' to projectCorrespondSiteServiceD and projectForwardSiteServiceD
# 23-Sep-2016 jdw  add content type 'em-structure-factors', 'em-sf'
# 19-Oct-2016 ep   add em-sf-convert-report to _contentTypeInfoBaseD
# 23-Oct-2016 jdw  add _siteGroupDataSetIdAssignmentD
# 08-Nov-2016 ep   Move default location of SITE_EM_DICT_PATH to resource directory
# 28-Nov-2016 ep   add 'dict-check-report-next' for V5RC dictionary report
#  5-Dec-2016 jw   deprecate _pdbeD -
# 12-Dec-2016 ep   For messaging services, use https for RCSB production, UCSD production, PDBj production
# 31-Jan-2017 jw   add content types model-legacy-rcsb, sf-legacy-rcsb, correspondence-legacy-rcsb
# 01-Feb-2017 ep   Add assembly-depinfo-update
# 02-Jun-2017 ep   Add PROJECT_CONTENTWS_SERVICE_DICTIONARY to configuration to map site_id to contentws service urls
# 11-Oct-2017 ep   Add deposition-info and deposition-store types with tar suffix
# 23-Oct-2017 jw   add session content types - disable all fallback behavior!
# 17-Jan-2018 ep   add SITE_DATASET_TEST_ID_ASSIGNMENT_DICTIONARY to support testing datasets that are outside normal assignment range
# 20-Jun-2019 my   add content type 'nmr-unified-data-nef' and 'nmr-unified-data-str'
# 27-Jun-2019 my   add content type 'nmr-unified-data-nef-report' and 'nmr-unified-data-str-report'
# 21-Feb-2020 ep   change 'nmr-unified-data-{nef,str}' to 'nmr-data-{nef,str}'
##
"""
Container for general and site-specific configuration data.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import sys
import traceback

# ----------------------------------------------------------------------------------------------
#  Try to import externally cached configuration options.  Gracefully ignore any errors.
try:
    from ConfigInfoFileCache import ConfigInfoFileCache  # pylint: disable=import-error
except:  # noqa: E722 pylint: disable=bare-except
    pass


class ConfigInfoData(object):
    """Provides access to shared and site-specific configuration information for the common
    deposition and annotation system.

    Configuration data is stored in a dictionary of key value pairs.

    Configuration data is defined in class ConfigInfoData().  Site-specific
    configuration data is selected from this class based on the value of the
    environmental variable WWPDB_SITE_ID.

    """

    #
    _contentTypeInfoD = {}
    _contentTypeInfoBaseD = {
        "model": (["pdbx", "pdb", "pdbml", "cifeps"], "model"),
        "model-emd": (["pdbx", "xml"], "model-emd"),
        "model-aux": (["pdbx"], "model-aux"),
        "model-legacy-rcsb": (["pdbx", "pdb"], "model-legacy-rcsb"),
        "structure-factors": (["pdbx", "mtz", "txt"], "sf"),
        "structure-factors-legacy-rcsb": (["pdbx", "mtz"], "sf-legacy-rcsb"),
        "nmr-data-config": (["json"], "nmr-data-config"),
        "nmr-data-nef": (["nmr-star", "pdbx"], "nmr-data-nef"),
        "nmr-data-str": (["nmr-star", "pdbx"], "nmr-data-str"),
        "nmr-data-nef-report": (["json"], "nmr-data-nef-report"),
        "nmr-data-str-report": (["json"], "nmr-data-str-report"),
        "nmr-restraints": (["any", "nmr-star", "amber", "amber-aux", "biosym", "cns", "cyana", "rosetta", "xplor", "xplor-nih", "pdb-mr", "mr"], "mr"),
        "nmr-chemical-shifts": (["nmr-star", "pdbx", "any"], "cs"),
        "nmr-chemical-shifts-raw": (["nmr-star", "pdbx"], "cs-raw"),
        "nmr-chemical-shifts-auth": (["nmr-star", "pdbx"], "cs-auth"),
        "nmr-chemical-shifts-upload-report": (["pdbx"], "nmr-chemical-shifts-upload-report"),
        "nmr-chemical-shifts-atom-name-report": (["pdbx"], "nmr-chemical-shifts-atom-name-report"),
        "nmr-shift-error-report": (["json"], "nmr-shift-error-report"),
        "nmr-bmrb-entry": (["nmr-star", "pdbx"], "nmr-bmrb-entry"),
        "nmr-harvest-file": (["tgz"], "nmr-harvest-file"),
        "nmr-peaks": (["any"], "nmr-peaks"),
        "nmr-nef": (["nmr-star", "pdbx"], "nmr-nef"),  # nmr-nef will be deprecated.
        "nmr-cs-check-report": (["html"], "nmr-cs-check-report"),
        "nmr-cs-xyz-check-report": (["html"], "nmr-cs-xyz-check-report"),
        "nmr-cs-path-list": (["txt"], "nmr-cs-path-list"),
        "nmr-cs-auth-file-name-list": (["txt"], "nmr-cs-auth-file-name-list"),
        "nmr-mr-path-list": (["json"], "nmr-mr-path-list"),
        "component-image": (["jpg", "png", "gif", "svg", "tif", "tiff"], "ccimg"),
        "component-definition": (["pdbx", "sdf"], "ccdef"),
        "em-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-volume"),
        "em-mask-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-mask-volume"),
        "em-additional-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-additional-volume"),
        "em-half-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-half-volume"),
        "em-raw-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-raw-volume"),
        "em-fsc-half-mask-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-fsc-half-mask-volume"),
        "em-fsc-map-model-mask-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-fsc-map-model-mask-volume"),
        "em-alignment-mask-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-alignment-mask-volume"),
        "em-focused-refinement-mask-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-focused-refinement-mask-volume"),
        "em-3d-classification-additional-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-3d-classification-additional-volume"),
        "em-focus-refinement-additional-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-focus-refinement-additional-volume"),
        "em-segmentation-volume": (["map", "ccp4", "mrc2000", "bcif"], "em-segmentation-volume"),
        "em-volume-wfcfg": (["json"], "em-volume-wfcfg"),
        "em-mask-volume-wfcfg": (["json"], "em-mask-volume-wfcfg"),
        "em-additional-volume-wfcfg": (["json"], "em-additional-volume-wfcfg"),
        "em-half-volume-wfcfg": (["json"], "em-half-volume-wfcfg"),
        "em-volume-report": (["json"], "em-volume-report"),
        "em-volume-header": (["xml"], "em-volume-header"),
        "em-model-emd": (["pdbx"], "em-model-emd"),
        "em-structure-factors": (["pdbx", "mtz"], "em-sf"),
        "emd-xml-header-report": (["txt"], "emd-xml-header-report"),
        "validation-report-depositor": (["pdf"], "valdep"),
        "seqdb-match": (["pdbx", "pic"], "seqdb-match"),
        "blast-match": (["xml"], "blast-match"),
        "seq-assign": (["pdbx"], "seq-assign"),
        "partial-seq-annotate": (["txt"], "partial-seq-annotate"),
        "seq-data-stats": (["pic"], "seq-data-stats"),
        "seq-align-data": (["pic"], "seq-align-data"),
        "pre-seq-align-data": (["pic"], "pre-seq-align-data"),
        "seqmatch": (["pdbx"], "seqmatch"),
        "mismatch-warning": (["pic"], "mismatch-warning"),
        "polymer-linkage-distances": (["pdbx", "json"], "poly-link-dist"),
        "polymer-linkage-report": (["html"], "poly-link-report"),
        "geometry-check-report": (["pdbx"], "geometry-check-report"),
        "chem-comp-link": (["pdbx"], "cc-link"),
        "chem-comp-assign": (["pdbx"], "cc-assign"),
        "chem-comp-assign-final": (["pdbx"], "cc-assign-final"),
        "chem-comp-assign-details": (["pic"], "cc-assign-details"),
        "chem-comp-depositor-info": (["pdbx"], "cc-dpstr-info"),
        "prd-search": (["pdbx"], "prd-summary"),
        "assembly-report": (["txt", "xml"], "assembly-report"),
        "assembly-assign": (["pdbx", "txt"], "assembly-assign"),
        "assembly-depinfo-update": (["txt"], "assembly-depinfo-update"),
        "interface-assign": (["xml"], "interface-assign"),
        "assembly-model": (["pdb", "pdbx"], "assembly-model"),
        "assembly-model-xyz": (["pdb", "pdbx"], "assembly-model-xyz"),
        "site-assign": (["pdbx"], "site-assign"),
        "dict-check-report": (["txt"], "dict-check-report"),
        "dict-check-report-r4": (["txt"], "dict-check-report-r4"),
        "dict-check-report-next": (["txt"], "dict-check-report-next"),
        "tom-complex-report": (["txt"], "tom-upload-report"),
        "tom-merge-report": (["txt"], "tom-merge-report"),
        "format-check-report": (["txt"], "format-check-report"),
        "misc-check-report": (["txt"], "misc-check-report"),
        "special-position-report": (["txt"], "special-position-report"),
        "merge-xyz-report": (["txt"], "merge-xyz-report"),
        "model-issues-report": (["json"], "model-issues-report"),
        "structure-factor-report": (["json"], "structure-factor-report"),
        "validation-report": (["pdf"], "val-report"),
        "validation-report-full": (["pdf"], "val-report-full"),
        "validation-report-slider": (["png", "svg"], "val-report-slider"),
        "validation-data": (["pdbx", "xml"], "val-data"),
        "validation-report-2fo-map-coef": (["pdbx"], "val-report-wwpdb-2fo-fc-edmap-coef"),
        "validation-report-fo-map-coef": (["pdbx"], "val-report-wwpdb-fo-fc-edmap-coef"),
        "validation-report-images": (["tar"], "val-report-images"),
        "map-xray": (["bcif"], "map-xray"),
        "map-2fofc": (["map"], "map-2fofc"),
        "map-fofc": (["map"], "map-fofc"),
        "map-omit-2fofc": (["map"], "map-omit-2fofc"),
        "map-omit-fofc": (["map"], "map-omit-fofc"),
        "sf-convert-report": (["pdbx", "txt"], "sf-convert-report"),
        "em-sf-convert-report": (["pdbx", "txt"], "em-sf-convert-report"),
        "dcc-report": (["pdbx", "txt"], "dcc-report"),
        "mapfix-header-report": (["json"], "mapfix-header-report"),
        "mapfix-report": (["txt"], "mapfix-report"),
        "secondary-structure-topology": (["txt"], "ss-topology"),
        "sequence-fasta": (["fasta", "fsa"], "fasta"),
        "messages-from-depositor": (["pdbx"], "messages-from-depositor"),
        "messages-to-depositor": (["pdbx"], "messages-to-depositor"),
        "notes-from-annotator": (["pdbx"], "notes-from-annotator"),
        "correspondence-to-depositor": (["txt"], "correspondence-to-depositor"),
        "correspondence-legacy-rcsb": (["pdbx"], "correspondence-legacy-rcsb"),
        "correspondence-info": (["pdbx"], "correspondence-info"),
        "map-header-data": (["json", "pic", "txt"], "map-header-data"),
        "deposit-volume-params": (["pic"], "deposit-volume-params"),
        "fsc": (["xml"], "fsc-xml"),
        "fsc-report": (["txt"], "fsc-report"),
        "res-est-fsc": (["xml"], "res-est-fsc"),
        "res-est-fsc-report": (["txt"], "res-est-fsc-report"),
        "map-model-fsc": (["xml"], "map-model-fsc"),
        "map-model-fsc-report": (["txt"], "map-model-fsc-report"),
        "em2em-report": (["txt"], "em2em-report"),
        "img-emdb": (["jpg", "png", "gif", "svg", "tif"], "img-emdb"),
        "img-emdb-report": (["txt"], "img-emdb-report"),
        "layer-lines": (["txt"], "layer-lines"),
        "auxiliary-file": (["any"], "aux-file"),
        "status-history": (["pdbx"], "status-history"),
        "virus-matrix": (["any"], "virus"),
        "parameter-file": (["any"], "parm"),
        "structure-def-file": (["any"], "struct"),
        "topology-file": (["any"], "topo"),
        "cmd-line-args": (["txt"], "cmd-line-args"),
        "sd-dat": (["any", "sd-dat"]),
        "sx-pr": (["any", "sx-pr"]),
        "sm-fit": (["any", "sm-fit"]),
        "deposition-info": (["pdbx", "json"], "deposition-info"),
        "deposition-store": (["tar"], "deposition-store"),
        #
        "bundle-session-archive": (["tar", "tgz"], "bundle-session-archive"),
        "bundle-session-deposit": (["tar", "tgz"], "bundle-session-deposit"),
        "bundle-session-upload": (["tar", "tgz"], "bundle-session-upload"),
        "bundle-session-tempdep": (["tar", "tgz"], "bundle-session-tempdep"),
        "bundle-session-uitemp": (["tar", "tgz"], "bundle-session-uitemp"),
        "bundle-session-workflow": (["tar", "tgz"], "bundle-session-workflow"),
        "session-backup": (["tar", "tgz"], "bundle-session-workflow"),
        #
        "manifest-session": (["json"], "manifest-session"),
        "manifest-session-bundle": (["json"], "manifest-session-bundle"),
        "any": (["any"], "any"),
    }
    """Base dictionary of supported file formats for each recognized content type.
       An acronym for each content type is included.  The acronym is used in the
       filename template.

       The above dictionary contains the cannonical list of file types recongnized by the system.

       We additionally define milestone variants of each content type to correspond to the following cases:

                     *-upload    -  content uploaded by a depositor and otherwise unmodified
                *-upload-convert -  content uploaded by a depositor and subjected to some update or formatted conversion
                     *-deposit   -  content produced at key transitions in the deposition process
                     *-annotate  -  content produced at key points during the annotation process
                     *-release   -  content published into the public archive
                     *-review    -  content consistent with public archive intended for depositor review

       Note that not all milestone are necessarilly meaningful for all content types, but all are defined
       for completeness.  Milestone content types are referenced by concatenation of the milestone with
       the content type (e.g. content type  model will have milestones model-upload, model-deposit,
       model-annotate, model-review, and model-release).
    """
    #
    _contentMilestoneL = ["upload", "upload-convert", "deposit", "annotate", "release", "review"]
    #
    _fileFormatExtensionD = {
        "pdbx": "cif",
        "pdb": "pdb",
        "cifeps": "cifeps",
        "pdbml": "xml",
        "nmr-star": "str",
        "gz": "gz",
        "tgz": "tgz",
        "mtz": "mtz",
        "html": "html",
        "jpg": "jpg",
        "png": "png",
        "svg": "svg",
        "gif": "gif",
        "tif": "tif",
        "tiff": "tiff",
        "sdf": "sdf",
        "ccp4": "ccp4",
        "mrc2000": "mrc",
        "pic": "pic",
        "txt": "txt",
        "xml": "xml",
        "pdf": "pdf",
        "map": "map",
        "bcif": "bcif",
        "amber": "amber",
        "amber-aux": "amber-aux",
        "biosym": "biosym",
        "cns": "cns",
        "cyana": "cyana",
        "rosetta": "rosetta",
        "xplor": "xplor",
        "xplor-nih": "xplor-nih",
        "pdb-mr": "mr",
        "mr": "mr",
        "json": "json",
        "fsa": "fsa",
        "fasta": "fasta",
        "any": "dat",
        "mdl": "mdl",
        "tar": "tar",
    }
    """Dictionary of recognized file formats and file name extensions"""

    #   WARNING -  changing the following assignments may have serious downstream consequences.
    #              Any modifications must agreed project-wide -
    _siteDataSetIdAssignmentD = {
        "WWPDB_DEPLOY_LEGACY_RU": (1000000001, 1000199999),
        "WWPDB_DEPLOY_PRODUCTION_RU": (1000200000, 1001200000),
        # 'WWPDB_DEPLOY_NEXT_RU': (1000200000, 1001200000),
        "WWPDB_DEPLOY_PRODUCTION_UCSD": (1001200001, 1001300000),
        "WWPDB_DEPLOY_PRODUCTION_BACKUP_RU": (1001310119, 1001350000),
        "WWPDB_DEPLOY_DEPGRP1_RU": (1001400001, 1001500000),
        "WWPDB_DEPLOY_DEPGRP2_RU": (1001400001, 1001500000),
        # 'PDBE_LEGACY': (1290000001, 1300000000), #PDBE legacy are incorporated into PDBE_PROD
        # 'PDBE_PROD': (1200000001, 1290000000),
        "PDBE_PROD": (1200000001, 1300000000),
        "PDBE_STG": (8211000001, 8212000000),
        "PDBE_DEV": (8233000001, 8234000000),
        "PDBE_EMDB": (8212000001, 8213000000),
        "PDBE_VAL": (900000000, 909999999),
        "WWPDB_DEPLOY_PRODUCTION_PDBJ": (1300000001, 1400000000),
        "WWPDB_DEPLOY_PRODUCTION_PDBC": (1400000001, 1500000000),
        # 'BMRB': (1400000001, 1500000000),
        # 'WWPDB_DEPLOY_TEST_RU': (8000200000, 8100000000),
        "WWPDB_DEPLOY_TEST_RU": (8000210000, 8000215000),
        "WWPDB_DEPLOY_ALPHA_RU": (8000220000, 8000230000),
        "WWPDB_DEPLOY_LCLTEST_RU": (8000230000, 8000231000),
        "WWPDB_DEPLOY_BETA_RU": (8000240000, 8000250000),
        "WWPDB_DEPLOY_VALSRV2_RU": (9100000000, 9101000000),
        "WWPDB_DEPLOY_VALSRV2_UCSD": (9101000000, 9102000000),
        "UNASSIGNED": (800000, 999999),
    }
    """Dictionary of site-level deposition data set identifier assignment ranges"""
    #
    _siteGroupDataSetIdAssignmentD = {"WWPDB_DEPLOY_DEPGRP1_RU": (1000000, 2000000), "WWPDB_DEPLOY_DEPGRP2_RU": (1000000, 2000000), "UNASSIGNED": (0000000, 1000000)}
    """Dictionary of site-level group deposition data set identifier assignment ranges"""

    #
    _siteDataSetTestIdAssignmentD = {
        "WWPDB_DEPLOY_LCLTEST_RU": (8000231000, 8000232000),
        "WWPDB_DEPLOY_TEST_RU": (8000215000, 8000220000),
    }
    """Dictionary of site-level IDs that can be used for creating test sessions. Do not add for production servers"""

    #
    _projectDepositSiteServiceD = {
        "WWPDB_DEPLOY_PRODUCTION_RU": "https://deposit.wwpdb.org/deposition",
        "WWPDB_DEPLOY_NEXT_RU": "https://deposit.wwpdb.org/deposition",
        "WWPDB_DEPLOY_LEGACY_RU": "https://deposit-legacy.wwpdb.org/deposition",
        "WWPDB_DEPLOY_PRODUCTION_UCSD": "https://deposit-rcsb-west.wwpdb.org/deposition",
        "WWPDB_DEPLOY_BETA_RU": "https://onedep-beta-dep-1.rcsb.rutgers.edu",
        "WWPDB_DEPLOY_PRODUCTION_PDBJ": "https://deposit-pdbj.wwpdb.org/deposition",
        "WWPDB_DEPLOY_PRODUCTION_PDBC": "https://deposit-pdbc.wwpdb.org/deposition",
        "PDBE_PROD": "https://deposit-pdbe.wwpdb.org/deposition",
        "PDBE_LEGACY": "https://deposit-pdbe.wwpdb.org/deposition",
        "PDBE_STG": "https://wwwdev.ebi.ac.uk/pdbe-da-staging/deposition",
        "PDBE_DEV": "https://wwwdev.ebi.ac.uk/pdbe-da/deposition",
        "PDBE_VAL": "https://validate-pdbe.wwpdb.org/validservice",
        # 'PDBE_DEV': 'https://dev.pdbe.org/deposition',
        "WWPDB_DEPLOY_ALPHA_RU": "https://da-dep-alpha-0.rcsb.rutgers.edu/deposition",
        "WWPDB_DEPLOY_TEST_RU": "https://wwpdb-deploy-test-1.wwpdb.org/deposition",
        "WWPDB_DEPLOY_VALSRV2_RU": "https://validate-rcsb-east.wwpdb.org/validservice",
        "WWPDB_DEPLOY_VALSRV2_UCSD": "https://validate-rcsb-west.wwpdb.org/validservice",
    }
    """Dictionary of well known project deposition service entry points"""

    _projectCorrespondSiteServiceD = {
        "WWPDB_DEPLOY_PRODUCTION_RU": "https://da-ann-1.rcsb.rutgers.edu/service/messaging/archive_msg",
        "WWPDB_DEPLOY_PRODUCTION_UCSD": "https://dna1.rcsb.org/service/messaging/archive_msg",
        "WWPDB_DEPLOY_LEGACY_RU": "https://da-legacy-ann-1.rcsb.rutgers.edu/service/messaging/archive_msg",
        "WWPDB_DEPLOY_PRODUCTION_PDBJ": "https://onedep-ann-1.pdbj.org/service/messaging/archive_msg",
        "WWPDB_DEPLOY_PRODUCTION_PDBC": "https://onedep-ann-pdbc.pdbj.org/service/messaging/archive_msg",
        "WWPDB_DEPLOY_ALPHA_RU": "https://da-ann-alpha-0.rcsb.rutgers.edu/service/messaging/archive_msg",
        "WWPDB_DEPLOY_BETA_RU": "http://onedep-beta-ann-1.rcsb.rutgers.edu/service/messaging/archive_msg",
        "WWPDB_DEPLOY_DEPGRP1_RU": "https://ann-group-2.rcsb.rutgers.edu/service/messaging/archive_msg",
        "WWPDB_DEPLOY_DEPGRP2_RU": "https://ann-group-2.rcsb.rutgers.edu/service/messaging/archive_msg",
        "WWPDB_DEPLOY_TEST_RU": "https://da-test-ann-1.rcsb.rutgers.edu/service/messaging/archive_msg",
        "PDBE_PROD": "https://deposit-pdbe.wwpdb.org/service/messaging/archive_msg",
        "PDBE_LEGACY": "https://deposit-pdbe.wwpdb.org/service/messaging/archive_msg",
        "PDBE_DEV": "https://wwwdev.ebi.ac.uk/pdbe-da/service/messaging/archive_msg",
    }
    """Dictionary of well known project correspondence archive service end points"""

    _projectForwardingSiteServiceD = {
        "WWPDB_DEPLOY_PRODUCTION_RU": "https://da-ann-1.rcsb.rutgers.edu/service/messaging/forward_msg",
        "WWPDB_DEPLOY_PRODUCTION_UCSD": "https://dna1.rcsb.org/service/messaging/forward_msg",
        "WWPDB_DEPLOY_LEGACY_RU": "https://da-legacy-ann-1.rcsb.rutgers.edu/service/messaging/forward_msg",
        "WWPDB_DEPLOY_PRODUCTION_PDBJ": "https://onedep-ann-1.pdbj.org/service/messaging/forward_msg",
        "WWPDB_DEPLOY_PRODUCTION_PDBC": "https://onedep-ann-pdbc.pdbj.org/service/messaging/forward_msg",
        "WWPDB_DEPLOY_ALPHA_RU": "https://da-ann-alpha-0.rcsb.rutgers.edu/service/messaging/forward_msg",
        "WWPDB_DEPLOY_BETA_RU": "https://onedep-beta-ann-1.rcsb.rutgers.edu/service/messaging/forward_msg",
        "WWPDB_DEPLOY_DEPGRP1_RU": "https://ann-group-2.rcsb.rutgers.edu/service/messaging/forward_msg",
        "WWPDB_DEPLOY_DEPGRP2_RU": "https://ann-group-2.rcsb.rutgers.edu/service/messaging/forward_msg",
        "WWPDB_DEPLOY_TEST_RU": "https://da-test-ann-1.rcsb.rutgers.edu/service/messaging/forward_msg",
        "PDBE_PROD": "https://deposit-pdbe.wwpdb.org/service/messaging/forward_msg",
        "PDBE_LEGACY": "https://deposit-pdbe.wwpdb.org/service/messaging/forward_msg",
        "PDBE_DEV": "https://wwwdev.ebi.ac.uk/pdbe-da/service/messaging/forward_msg",
    }
    """Dictionary of well known project message forwarding service end points"""

    _regions = {"pdbe": ["europe", "africa", "antarctica"], "pdbj": ["asia", "middle east"], "rcsb": ["north america", "south america", "oceania"]}
    """Dictionary of geographical locations for each site"""

    _production_sites = {"pdbe": "PDBE_PROD", "pdbj": "WWPDB_DEPLOY_PRODUCTION_PDBJ", "rcsb": "WWPDB_DEPLOY_PRODUCTION_RU", "pdbc": "WWPDB_DEPLOY_PRODUCTION_PDBC"}
    """names of sites used in production"""

    # subjects for messages - used in the depUI and communication
    _message_subjects = {
        "general": ["Other"],
        "approval": ["Approval without corrections", "Approval with corrections"],
        "meta corrections": ["Other corrections"],
        "unlock": ["Re-upload files"],
        "release": ["Release request"],
        "release_with_citation": ["Release with citation update"],
        "citation": ["Citation update"],
        "pre-submission": [
            "File upload issue",
            "Submission issue",
            "General question",
        ],
        "withdrawal": ["Withdrawal"],
        "hold extension": ["Hold expiration"],
        "major issues": ["Response to issues"],
    }

    _communication_release_message_subjects = []
    _communication_release_message_subjects.extend(_message_subjects.get("release"))
    _communication_release_message_subjects.extend(_message_subjects.get("release_with_citation"))
    _communication_release_message_subjects.extend(_message_subjects.get("citation"))

    # mmCIF dictionary
    _pdbx_dictionary_name_dict = {"ARCHIVE_CURRENT": "mmcif_pdbx_v50", "ARCHIVE_NEXT": "mmcif_pdbx_v50", "DEPOSIT": "mmcif_pdbx_v5_next"}

    # CCD and PRD variables
    _ref_data_proj_names = {"cvs_path": "/cvs-ligands", "ccd": "ligand-dict-v3", "prd": "prd-v3", "prdcc": "prdcc-v3", "prd_family": "family-v3"}

    _projectContentWSiteServiceD = {
        "WWPDB_DEPLOY_PRODUCTION_RU": "https://onedep-contentws-rcsb.wwpdb.org",
        "WWPDB_DEPLOY_LEGACY_RU": "https://onedep-contentws-rcsb.wwpdb.org",
        "WWPDB_DEPLOY_TEST_RU": "https://da-test-1-dep.rcsb.rutgers.edu",
        "PDBE_DEV": "https://dev.pdbe.org",
        "PDBE_STG": "https://dev.pdbe.org",
        "PDBE_PROD": "https://deposit-pdbe.wwpdb.org",
        "WWPDB_DEPLOY_PRODUCTION_PDBJ": "https://onedep-contentws-pdbj.wwpdb.org",
        "WWPDB_DEPLOY_PRODUCTION_PDBC": "https://onedep-contentws-pdbc.wwpdb.org",
        "WWPDB_DEPLOY_ALPHA_RU": "https://da-ws-alpha-0.rcsb.rutgers.edu",
        # 'PDBE_LEGACY': 'https://deposit-pdbe.wwpdb.org/service/messaging/archive_msg',
    }
    """Dictionary of well known contentws forwarding service urls"""

    _valRelCutoffD = {"start": "Fri:09:00:00", "end": "Fri:23:59:59"}
    """Local cutoff blackout weekday/time for producing validation reports"""
    #
    # ----------------------------------------------------------------------------------------------
    #   --- PLEASE remove the following unused class-level assignments ---
    #
    _configSiteDeployPath = "/net/anypath"
    _configSiteToolsDeployPath = os.path.join(_configSiteDeployPath, "tools-centos-6")
    _configSitePackagesDeployPath = os.path.join(_configSiteDeployPath, "tools-centos-6", "packages")
    _configSiteMachineName = "http://localhost:8000"

    def __init__(self, siteId=None, verbose=True, log=sys.stderr, useCache=True):
        # """The list of configuration key names supported by all sites.
        # """
        self.__D = {}
        self.__siteId = siteId
        self.__verbose = verbose
        self.__debug = False
        self.__lfh = log
        #
        if self.__siteId is None:
            self.__siteId = str(os.getenv("WWPDB_SITE_ID", None)).upper()
            """The site identification is obtained from the environmental variable `WWPDB_SITE_ID`
            """

        if self.__verbose and self.__siteId is None:
            self.__lfh.write(
                "%s.%s WARNING - no siteId assigned in constructor or found in the environemt (WWPDB_SITE_ID).\n" % (self.__class__.__name__, sys._getframe().f_code.co_name)
            )

        #
        # -------------------------------------------------------------------------------------------------------
        # First, check for externally cached configuration options.  If these not found (i.e. on error), OR
        # if no cached options are found then use the locally defined fallback options (e.g. self.__setup())
        #
        # Note that options defined as class level constants  (e.g. 'FILE_FORMAT_EXTENSION_DICTIONARY',
        #    'CONTENT_TYPE_DICTIONARY', 'CONTENT_MILESTONE_LIST', 'CONTENT_TYPE_BASE_DICTIONARY', ...) are
        #     NOT externally CACHED.
        #
        if useCache:
            readCache = False
            try:
                cls = ConfigInfoFileCache()
                cacheD = cls.getConfigDictionary(siteId=self.__siteId)
                if self.__debug:
                    self.__lfh.write(
                        "%s.%s Imported cached configuration dictionary length %d for site %s\n"
                        % (self.__class__.__name__, sys._getframe().f_code.co_name, len(cacheD), self.__siteId)
                    )
                if len(cacheD) > 0:
                    readCache = True
                    self.__D = cacheD
            except:  # noqa: E722 pylint: disable=bare-except
                if self.__debug:
                    self.__lfh.write("%s.%s failed importing cache for site %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name, self.__siteId))
                    traceback.print_exc(file=self.__lfh)
                readCache = False

            #
            # Use fall back configuration options for now  -- to be deprecated in the future --
            #
            if not readCache and self.__siteId is not None and self.__debug:
                self.__lfh.write("%s.%s No configuration for site %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name, self.__siteId))
                # self.__setup(self.__siteId)
                # if self.__verbose:
                #    self.__lfh.write("%s.%s Cache not used imported fallback configuration dictionary length %d for site %s\n" %
                #                     (self.__class__.__name__, sys._getframe().f_code.co_name, len(self.__D), self.__siteId))
        else:
            if self.__siteId is not None and self.__debug:
                self.__lfh.write("%s.%s No configuration for site %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name, self.__siteId))
                # self.__setup(self.__siteId)
                # if self.__verbose:
                #    self.__lfh.write("%s.%s Imported fallback configuration dictionary length %d for site %s\n" %
                #                     (self.__class__.__name__, sys._getframe().f_code.co_name, len(self.__D), self.__siteId))
        #
        # -------------------------------------------------------------------------------------------------------
        #  Add other class-level - common configuration components - these configuration options are tightly coupled
        #  to project operation and should remain as static declarations in this class module.
        #
        self.__addMilestoneVariants()
        self.__D["FILE_FORMAT_EXTENSION_DICTIONARY"] = ConfigInfoData._fileFormatExtensionD
        self.__D["CONTENT_TYPE_DICTIONARY"] = ConfigInfoData._contentTypeInfoD
        self.__D["CONTENT_MILESTONE_LIST"] = ConfigInfoData._contentMilestoneL
        self.__D["CONTENT_MILESTONE_ARCHIVE_LIST"] = [t for t in ConfigInfoData._contentMilestoneL if t != "upload-convert"]
        self.__D["CONTENT_TYPE_BASE_DICTIONARY"] = ConfigInfoData._contentTypeInfoBaseD
        self.__D["SITE_DATASET_ID_ASSIGNMENT_DICTIONARY"] = ConfigInfoData._siteDataSetIdAssignmentD
        self.__D["SITE_DATASET_TEST_ID_ASSIGNMENT_DICTIONARY"] = ConfigInfoData._siteDataSetTestIdAssignmentD
        self.__D["SITE_GROUP_DATASET_ID_ASSIGNMENT_DICTIONARY"] = ConfigInfoData._siteGroupDataSetIdAssignmentD
        self.__D["PROJECT_DEPOSIT_SERVICE_DICTIONARY"] = ConfigInfoData._projectDepositSiteServiceD
        self.__D["PROJECT_CORRESPOND_SERVICE_DICTIONARY"] = ConfigInfoData._projectCorrespondSiteServiceD
        self.__D["PROJECT_FORWARDING_SERVICE_DICTIONARY"] = ConfigInfoData._projectForwardingSiteServiceD
        self.__D["PROJECT_CONTENTWS_SERVICE_DICTIONARY"] = ConfigInfoData._projectContentWSiteServiceD
        self.__D["PROJECT_VAL_REL_CUTOFF"] = ConfigInfoData._valRelCutoffD
        self.__D["REGIONS"] = ConfigInfoData._regions
        self.__D["PRODUCTION_SITES"] = ConfigInfoData._production_sites
        self.__D["MESSAGE_SUBJECTS"] = ConfigInfoData._message_subjects
        self.__D["COMMUNICATION_RELEASE_MESSAGE_SUBJECTS"] = ConfigInfoData._communication_release_message_subjects
        self.__D["PDBX_DICTIONARY_NAME_DICT"] = ConfigInfoData._pdbx_dictionary_name_dict
        self.__D["SITE_REFDATA_CVS_PATH"] = ConfigInfoData._ref_data_proj_names.get("cvs_path")
        self.__D["SITE_REFDATA_PROJ_NAME_CC"] = ConfigInfoData._ref_data_proj_names.get("ccd")
        self.__D["SITE_REFDATA_PROJ_NAME_PRD"] = ConfigInfoData._ref_data_proj_names.get("prd")
        self.__D["SITE_REFDATA_PROJ_NAME_PRDCC"] = ConfigInfoData._ref_data_proj_names.get("prdcc")
        self.__D["SITE_REFDATA_PROJ_NAME_PRD_FAMILY"] = ConfigInfoData._ref_data_proj_names.get("prd_family")

    def getConfigDictionary(self):
        return self.__D

    def __addMilestoneVariants(self):
        """Update base content dictionary with content milestone variants."""
        ConfigInfoData._contentTypeInfoD = {}
        for k, v in ConfigInfoData._contentTypeInfoBaseD.items():
            ConfigInfoData._contentTypeInfoD[k] = v
            for ms in ConfigInfoData._contentMilestoneL:
                kM = k + "-" + ms
                acM = v[1] + "-" + ms
                ConfigInfoData._contentTypeInfoD[kM] = (v[0], acM)
