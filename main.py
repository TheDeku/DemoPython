
from bcolors import bcolors
from processData import ProcessData
from static_config import staticConfig

ProcessData.processCustomers(ProcessData)
ProcessData.processEquipment(ProcessData)

ProcessData.processCustomerOut(ProcessData)
ProcessData.processEquipmentOut(ProcessData)


ProcessData.processJobs(ProcessData,'completed')

print(f"{bcolors.OKGREEN}Number of calls ST API: {staticConfig.APICALLED}{bcolors.ENDC}")
print(f"{bcolors.OKGREEN}Done{bcolors.ENDC}")







