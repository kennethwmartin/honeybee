# By Mostapha Sadeghipour Roudsari
# Sadeghipour@gmail.com
# Honeybee started by Mostapha Sadeghipour Roudsari is licensed
# under a Creative Commons Attribution-ShareAlike 3.0 Unported License.

"""
Read Daysim Annual Profiles

-
Provided by Honeybee 0.0.54

    Args:
        _annualProfiles: Address to a valid *_intgain.csv generated by daysim.
    Returns:
        occupancyProfile: Lists of annual occupancy profiles if any
        shadingProfiles Lists of annual shading profiles if any
        lightingControlProfiles: Lists of annual lighting switch profiles if any
        dgpProfile: Lists of annual daylight glare probability profiles if any
"""
ghenv.Component.Name = "Honeybee_Daysim Annual Profiles"
ghenv.Component.NickName = 'DSAnnualProfiles'
ghenv.Component.Message = 'VER 0.0.54\nAUG_25_2014'
ghenv.Component.Category = "Honeybee"
ghenv.Component.SubCategory = "04 | Daylight | Daylight"
#compatibleHBVersion = VER 0.0.55\nAUG_25_2014
#compatibleLBVersion = VER 0.0.58\nAUG_20_2014
try: ghenv.Component.AdditionalHelpFromDocStrings = "5"
except: pass


from System import Object
import Grasshopper.Kernel as gh
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

occupancyProfile = DataTree[Object]()
shadingProfiles = DataTree[Object]()
lightingControlProfiles = DataTree[Object]()
dgpProfile = DataTree[Object]()

if _annualProfiles.DataCount!=0 and _annualProfiles.Branch(0)[0]!=None:
    for branchCount in range(_annualProfiles.BranchCount):
        # open the file
        filePath = _annualProfiles.Branch(branchCount)[0]
        with open(filePath, "r") as inf:
            
            for lineCount, line in enumerate(inf):
                if lineCount == 3:
                    headings = line.strip().split(",")[3:]
                    resultDict = {}
                    for heading in range(len(headings)):
                        resultDict[heading] = []
                elif lineCount> 3:
                    results = line.strip().split(",")[3:]
                    for resCount, result in enumerate(results):
                        try:
                            resultDict[resCount].append(float(result))
                        except:
                            pass
            occupancyHeading = ["key:location/dataType/units/frequency/startsAt/endsAt",
                                " ", "Occupancy Profile", "0 = Absent, 1 = Present", "Hourly",
                                (1, 1, 1), (12, 31, 24)]
            lightingHeading = ["key:location/dataType/units/frequency/startsAt/endsAt",
                                " ", "Lighting Switch Profile", "0 = Off, 1 = On", "Hourly",
                                (1, 1, 1), (12, 31, 24)]
            shadingHeading = ["key:location/dataType/units/frequency/startsAt/endsAt",
                                " ", "Shading Profile", "0 = Up, 1 = Down", "Hourly",
                                (1, 1, 1), (12, 31, 24)]
            occCounter = 0
            shadingCounter = 0
            lightingCounter = 0
            for headingCount, heading in enumerate(headings):
                if heading.strip().startswith("occ"):
                    p = GH_Path(branchCount, occCounter)
                    occupancyProfile.AddRange(occupancyHeading + resultDict[headingCount], p)
                    occCounter += 1
                if heading.strip().startswith("light"):
                    p = GH_Path(branchCount, lightingCounter)
                    lightingControlProfiles.AddRange(lightingHeading + resultDict[headingCount], p)
                    lightingCounter += 1
                if heading.strip().startswith("blind"):
                    p = GH_Path(branchCount, shadingCounter)
                    shadingProfiles.AddRange(shadingHeading + resultDict[headingCount], p)
                    shadingCounter += 1
            dgpProfile = "[place holder]"
