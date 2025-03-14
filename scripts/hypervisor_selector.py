import sys
from enum import Enum

class Hypervisor(Enum):
    VIRTUALBOX = "VirtualBox"
    KVM = "KVM"

def select_hypervisor():
    hypervisors = list(Hypervisor)
    print("Available hypervisors:")
    for index, hv in enumerate(hypervisors, start=1):
        print(f"{index}. {hv.value}")
    
    valid_choices = {str(i) for i in range(1, len(hypervisors) + 1)}
    while (choice := input(f"Select an option (1-{len(hypervisors)}): ")) not in valid_choices:
        print("Invalid option.")
    
    return hypervisors[int(choice) - 1]
