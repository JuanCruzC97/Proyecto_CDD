# Prediction-Discrete: Na?ve Bayes
rm(list=ls())
library(readxl)   # read Excel files
library(e1071)
library(car)      #vif
library(readr)

setwd("~/GitHub/Proyecto_CDD")
getwd()
dat <- read_csv("./Proyecto A/00 - Creación Dataset y Variables/Dataset_Modelos.csv")

setwd(getwd())


# Functions
accu <- function(yp,yT) {ct=table(yp,yT);x=(ct[1,1]+ct[2,2])/sum(ct);return(x)}
sens <- function(yp,yT) {ct=table(yp,yT);x=ct[2,2]/(ct[2,2]+ct[1,2]);return(x)}
specif <- function(yp,yT) {ct=table(yp,yT);x=ct[1,1]/(ct[1,1]+ct[2,1]);return(x)}

# read data
#rm(list=ls())

#elimino las variables que no entran al modelo

names(dat)
#creo un vector con las columnas que voy a eliminar
drop<-c("...1","url","scheme" ,"domain_complete","domain","subdomain","suffix"
        ,"domain_subdomain","path","suffix2"  )

dat = dat[,!(names(dat) %in% drop)]
# Split sample: Learn-Test
n = floor(0.8*nrow(dat))
set.seed(001)
Lind = sample(seq_len(nrow(dat)),size = n) 
datL = dat[Lind,]
datT = dat[-Lind,]
xL = datL[,!(names(datL)=="phishing")]
yL = as.factor(datL$phishing)
xT = datT[,!(names(datT)=="phishing")]
yT = as.factor(datT$phishing)


# Na?ve Bayes
yp = predict(naiveBayes(xL,yL),xT)
ct = table(yp,yT);ct;accu(yp,yT);sens(yp,yT);specif(yp,yT)
length(yp)
length(yT)
yT['resultado_test']<-yp
