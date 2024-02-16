import HLStatus
import sys
LogServer = sys.argv[1]
LogDB = sys.argv[2]
APID = sys.argv[3]
LogAccountName = sys.argv[4]
LogUser = sys.argv[5]
LogPwd = sys.argv[6]

HLStatus.UpdateHLStatus(APID,"Stepid96","Skipped","Environmental Setup is skipped since Installation is skipped",LogServer,LogDB,LogUser,LogPwd)
HLStatus.UpdateHLStatus(APID,"Stepid97","Skipped","Installation is skipped since Oracle Installation is skipped",LogServer,LogDB,LogUser,LogPwd)
HLStatus.UpdateHLStatus(APID,"Stepid98","Skipped","PostCheck is skipped since Oracle Installation is skipped",LogServer,LogDB,LogUser,LogPwd)
print "0"
print "ExitDesc: HLStatus Updated Successfully."