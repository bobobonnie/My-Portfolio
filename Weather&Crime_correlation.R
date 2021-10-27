library(dplyr)
library(tidyr)
library(stringr)
library(ggplot2)

# read csv data
## weather in sheffield
ukweather<-read.csv("Sheffield_weather.csv")
## police data of south-yorkshire
policeData_201801<-read.csv("2018-01-south-yorkshire-street.csv")
policeData_201802<-read.csv("2018-02-south-yorkshire-street.csv")
policeData_201803<-read.csv("2018-03-south-yorkshire-street.csv")
policeData_201804<-read.csv("2018-04-south-yorkshire-street.csv")
policeData_201805<-read.csv("2018-05-south-yorkshire-street.csv")
policeData_201806<-read.csv("2018-06-south-yorkshire-street.csv")
policeData_201807<-read.csv("2018-07-south-yorkshire-street.csv")
policeData_201808<-read.csv("2018-08-south-yorkshire-street.csv")
policeData_201809<-read.csv("2018-09-south-yorkshire-street.csv")
policeData_201810<-read.csv("2018-10-south-yorkshire-street.csv")
policeData_201811<-read.csv("2018-11-south-yorkshire-street.csv")
policeData_201812<-read.csv("2018-12-south-yorkshire-street.csv")
policeData_201901<-read.csv("2019-01-south-yorkshire-street.csv")
policeData_201902<-read.csv("2019-02-south-yorkshire-street.csv")
policeData_201903<-read.csv("2019-03-south-yorkshire-street.csv")
policeData_201904<-read.csv("2019-04-south-yorkshire-street.csv")
policeData_201905<-read.csv("2019-05-south-yorkshire-street.csv")
policeData_201906<-read.csv("2019-06-south-yorkshire-street.csv")
policeData_201907<-read.csv("2019-07-south-yorkshire-street.csv")
policeData_201908<-read.csv("2019-08-south-yorkshire-street.csv")
policeData_201909<-read.csv("2019-09-south-yorkshire-street.csv")
policeData_201910<-read.csv("2019-10-south-yorkshire-street.csv")
policeData_201911<-read.csv("2019-11-south-yorkshire-street.csv")
policeData_201912<-read.csv("2019-12-south-yorkshire-street.csv")
policeData_202001<-read.csv("2020-01-south-yorkshire-street.csv")
policeData_202002<-read.csv("2020-02-south-yorkshire-street.csv")
policeData_202003<-read.csv("2020-03-south-yorkshire-street.csv")
policeData_202004<-read.csv("2020-04-south-yorkshire-street.csv")
policeData_202005<-read.csv("2020-05-south-yorkshire-street.csv")
policeData_202006<-read.csv("2020-06-south-yorkshire-street.csv")
policeData_202007<-read.csv("2020-07-south-yorkshire-street.csv")
policeData_202008<-read.csv("2020-08-south-yorkshire-street.csv")
policeData_202009<-read.csv("2020-09-south-yorkshire-street.csv")
policeData_202010<-read.csv("2020-10-south-yorkshire-street.csv")
policeData_202011<-read.csv("2020-11-south-yorkshire-street.csv")
View(policeData_201801)
# combine 2018 data
CrimeData2018 <- rbind(policeData_201801,policeData_201802,policeData_201803,policeData_201804,policeData_201805,policeData_201806,
                       policeData_201807,policeData_201808,policeData_201809,policeData_201810,policeData_201811,policeData_201812)
# combine 2019 data
CrimeData2019 <- rbind(policeData_201901,policeData_201902,policeData_201903,policeData_201904,policeData_201905,policeData_201906,
                       policeData_201907,policeData_201908,policeData_201909,policeData_201910,policeData_201911,policeData_201912)
# combine 2020 data
CrimeData2020 <- rbind(policeData_202001,policeData_202002,policeData_202003,policeData_202004,policeData_202005,policeData_202006,
                       policeData_202007,policeData_202008,policeData_202009,policeData_202010,policeData_202011)

# check how many Crime Type is N.A.
sum(is.na(CrimeData2018$Crime.type))
sum(is.na(CrimeData2019$Crime.type))
sum(is.na(CrimeData2020$Crime.type))

# filter data for Sheffield
SheffieldCrime2018<-filter(CrimeData2018,grepl('Sheffield',LSOA.name)) 
SheffieldCrime2019<-filter(CrimeData2019,grepl('Sheffield',LSOA.name)) 
SheffieldCrime2020<-filter(CrimeData2020,grepl('Sheffield',LSOA.name))

# the UK police data has the month format of "2018-01"
# we need the year and month column to be "2018" and "1"
SheffieldCrime2018<-separate(data = SheffieldCrime2018, col = Month, into = c("Year", "Month"), sep = "\\-")
SheffieldCrime2019<-separate(data = SheffieldCrime2019, col = Month, into = c("Year", "Month"), sep = "\\-")
SheffieldCrime2020<-separate(data = SheffieldCrime2020, col = Month, into = c("Year", "Month"), sep = "\\-")

# remove the leading 0s with month
SheffieldCrime2018$Month <- str_remove(SheffieldCrime2018$Month,"^0+") %>%  as.integer(SheffieldCrime2018$Month)
SheffieldCrime2019$Month <- str_remove(SheffieldCrime2019$Month,"^0+") %>%  as.integer(SheffieldCrime2019$Month)
SheffieldCrime2020$Month <- str_remove(SheffieldCrime2020$Month,"^0+") %>%  as.integer(SheffieldCrime2020$Month)

# filtering "Violent Crimes" in "Sheffield" for each year
# "Violent Crimes" includes "Criminal damage and arson", "Robbery" and "Violence and sexual offences"
SheffieldViolentCrime2018 <- SheffieldCrime2018 %>% filter(Crime.type=="Criminal damage and arson"|Crime.type=="Robbery"|Crime.type=="Violence and sexual offences")
SheffieldViolentCrime2019 <- SheffieldCrime2019 %>% filter(Crime.type=="Criminal damage and arson"|Crime.type=="Robbery"|Crime.type=="Violence and sexual offences")
SheffieldViolentCrime2020 <- SheffieldCrime2020 %>% filter(Crime.type=="Criminal damage and arson"|Crime.type=="Robbery"|Crime.type=="Violence and sexual offences")

SheffieldDrugCrime2018 <- SheffieldCrime2018 %>% filter(Crime.type=="Drugs")
SheffieldDrugCrime2019 <- SheffieldCrime2019 %>% filter(Crime.type=="Drugs")
SheffieldDrugCrime2020 <- SheffieldCrime2020 %>% filter(Crime.type=="Drugs")

SheffieldVehicleCrime2018 <- SheffieldCrime2018 %>% filter(Crime.type=="Vehicle crime")
SheffieldVehicleCrime2019 <- SheffieldCrime2019 %>% filter(Crime.type=="Vehicle crime")
SheffieldVehicleCrime2020 <- SheffieldCrime2020 %>% filter(Crime.type=="Vehicle crime")

# correlation data
ukweather2018 <- ukweather %>% filter(ukweather$yyyy=="2018") 
ukweather2019 <- ukweather %>% filter(ukweather$yyyy=="2019")
ukweather2020 <- ukweather %>% filter(ukweather$yyyy=="2020")

# rename columns, because we will do the joining later
names(ukweather2018)[1]<-"Year"
names(ukweather2018)[2]<-"Month"
names(ukweather2019)[1]<-"Year"
names(ukweather2019)[2]<-"Month"
names(ukweather2020)[1]<-"Year"
names(ukweather2020)[2]<-"Month"

# count the total number of each crimes
SheffieldViolentCrimeSum2018 <- SheffieldViolentCrime2018 %>% group_by(Month) %>% summarise(TotalViolentCrime=n())
SheffieldDrugCrimeSum2018 <- SheffieldDrugCrime2018 %>% group_by(Month) %>% summarise(TotalDrugCrime=n()) 
SheffieldVehicleCrimeSum2018 <- SheffieldVehicleCrime2018 %>% group_by(Month) %>% summarise(TotalVehicleCrime=n()) 

SheffieldViolentCrimeSum2019 <- SheffieldViolentCrime2019 %>% group_by(Month) %>% summarise(TotalViolentCrime=n())
SheffieldDrugCrimeSum2019 <- SheffieldDrugCrime2019 %>% group_by(Month) %>% summarise(TotalDrugCrime=n()) 
SheffieldVehicleCrimeSum2019 <- SheffieldVehicleCrime2019 %>% group_by(Month) %>% summarise(TotalVehicleCrime=n()) 

SheffieldViolentCrimeSum2020 <- SheffieldViolentCrime2020 %>% group_by(Month) %>% summarise(TotalViolentCrime=n())
SheffieldDrugCrimeSum2020 <- SheffieldDrugCrime2020 %>% group_by(Month) %>% summarise(TotalDrugCrime=n()) 
SheffieldVehicleCrimeSum2020 <- SheffieldVehicleCrime2020 %>% group_by(Month) %>% summarise(TotalVehicleCrime=n()) 

# join data (weather and crime data)
cor2018<-merge(ukweather2018, SheffieldViolentCrimeSum2018, by = "Month")
cor2018<-merge(cor2018, SheffieldDrugCrimeSum2018, by = "Month")
cor2018<-merge(cor2018, SheffieldVehicleCrimeSum2018, by = "Month")

cor2019<-merge(ukweather2019, SheffieldViolentCrimeSum2019, by = "Month")
cor2019<-merge(cor2019, SheffieldDrugCrimeSum2019, by = "Month")
cor2019<-merge(cor2019, SheffieldVehicleCrimeSum2019, by = "Month")

cor2020<-merge(ukweather2020, SheffieldViolentCrimeSum2020, by = "Month")
#library(stringr)cor2020<-merge(cor2020, SheffieldDrugCrimeSum2020, by = "Month")
cor2020<-merge(cor2020, SheffieldVehicleCrimeSum2020, by = "Month")

cor(cor2018[c(3,7,6,8,9,10)], method="spearman")
cor(cor2019[c(3,7,6,8,9,10)], method="spearman")
cor(cor2020[c(3,7,6,8,9,10)], method="spearman")

# plots-weather 
## mean monthly temperature
ggplot(ukweather,aes(x=mm, y=(tmax+tmin)/2,label=(tmax+tmin)/2))+geom_line() +geom_point()+geom_text(hjust=1,vjust=-1)+ facet_grid(ukweather$yyyy) + scale_x_continuous(breaks=seq(2,12,3))+
  labs(x="Month", y="Mean Monthly Temperature (°C)",
       title='Mean Monthly Temperature in Sheffield', 
       subtitle = 'Compared by 2018, 2019 and 2020',
       caption='Historical monthly data from Sheffield meteorological stations')

## monthly max temperature
ggplot(ukweather,aes(x=mm, y=tmax,label=tmax))+geom_line() +geom_point()+geom_text(hjust=1,vjust=-1)+ facet_grid(ukweather$yyyy) + scale_x_continuous(breaks=seq(2,12,3))+ scale_y_continuous(limit = c(5, 30))+
  labs(x="Month", y="Monthly Max Temperature (°C)",
       title='Monthly Highest Temperature in Sheffield', 
       subtitle = 'Compared by 2018, 2019 and 2020',
       caption='Historical monthly data from Sheffield meteorological stations')

## mean monthly sunhours
ggplot(ukweather,aes(x=mm, y=sun,label=sun))+geom_line() +geom_point()+geom_text(hjust=1,vjust=-1)+ facet_grid(ukweather$yyyy) + scale_x_continuous(breaks=seq(2,12,3))+ scale_y_continuous(limit = c(0, 300))+
  labs(x="Month", y="Total sunshine duration",
       title='Monthly Sunhours in Sheffield', 
       subtitle = 'Compared by 2018, 2019 and 2020',
       caption='Historical monthly data from Sheffield meteorological stations')

## Total monthly rain
ggplot(ukweather,aes(x=mm, y=rain,label=rain))+geom_line() +geom_point()+geom_text(hjust=1,vjust=-1)+ facet_grid(ukweather$yyyy) + scale_x_continuous(breaks=seq(2,12,3))+ scale_y_continuous(limit = c(0, 250))+
  labs(x="Month", y="Total Monthly Rain(mm)",
       title='Total Monthly Rain in Sheffield', 
       subtitle = 'Compared by 2018, 2019 and 2020',
       caption='Historical monthly data from Sheffield meteorological stations')


# plots-violent crime
## Sheffield violent crime 2018, by crime type
ggplot(SheffieldViolentCrime2018, aes(Month))+geom_bar(aes(fill=Crime.type))+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Violent Crimes",
       title="2018 Monthly Violent Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_fill_discrete(name = "Crime Type")+ 
  scale_y_continuous(limit = c(0, 2500))+ 
  scale_fill_brewer(palette="Set3")

## Sheffield violent crime 2019, by crime type
ggplot(SheffieldViolentCrime2019, aes(Month))+geom_bar(aes(fill=Crime.type))+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Violent Crimes",
       title="2019 Monthly Violent Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_fill_discrete(name = "Crime Type")+ 
  scale_y_continuous(limit = c(0, 2500))+ 
  scale_fill_brewer(palette="Set3")

## Sheffield violent crime 2020, by crime type
ggplot(SheffieldViolentCrime2020, aes(Month))+geom_bar(aes(fill=Crime.type))+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Violent Crimes",
       title="2020 Monthly Violent Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_fill_discrete(name = "Crime Type")+ 
  scale_y_continuous(limit = c(0, 2500))+ 
  scale_fill_brewer(palette="Set3")


# plots-vehicle crime
## Sheffield vehicle crime 2018, by crime type
ggplot(SheffieldVehicleCrime2018, aes(Month))+geom_bar(fill="#73C6B6")+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Vehicle Crimes",
       title="2018 Monthly Vehicle Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_y_continuous(limit = c(0, 750))

## Sheffield vehicle crime 2019, by crime type
ggplot(SheffieldVehicleCrime2019, aes(Month))+geom_bar(fill="#73C6B6")+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Vehicle Crimes",
       title="2019 Monthly Vehicle Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_y_continuous(limit = c(0, 750))

## Sheffield vehicle crime 2020, by crime type
ggplot(SheffieldVehicleCrime2020, aes(Month))+geom_bar(fill="#73C6B6")+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Vehicle Crimes",
       title="2020 Monthly Vehicle Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_y_continuous(limit = c(0, 750))

# plots-drugs crime
## Sheffield drugs crime 2018, by crime type
ggplot(SheffieldDrugCrime2018, aes(Month))+geom_bar(fill="#85C1E9")+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Drugs Crimes",
       title="2018 Monthly Drug Crimes in Sheffield",
       caption="The UK Police Data") + 
  scale_y_continuous(limit = c(0, 250))

## Sheffield drugs crime 2019, by crime type
ggplot(SheffieldDrugCrime2019, aes(Month))+geom_bar(fill="#85C1E9")+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", y="Number of Drugs Crimes",
       title="2019 Monthly Drug Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_y_continuous(limit = c(0, 250))

## Sheffield drugs crime 2020, by crime type
ggplot(SheffieldDrugCrime2020, aes(Month))+geom_bar(fill="#85C1E9")+ scale_x_continuous(breaks=seq(1,12,1))+
  labs(x="Month", 
       y="Number of Drugs Crimes",
       title="2020 Monthly Drug Crimes in Sheffield",
       caption="The UK Police Data")+
  scale_y_continuous(limit = c(0, 250))


