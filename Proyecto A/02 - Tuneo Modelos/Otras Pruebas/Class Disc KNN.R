# Prediction-Discrete: K Nearest Neighbour
rm(list=ls())
library(readr)
library(dplyr)
library(readxl)
library(class)    #KNN
library(car)      #vif
dat <- read_excel("Discrim01 spam.xlsx")
dat <- read_csv("Dataset_Modelos.csv")
View(dat)
dir=dirname('../'+rstudioapi::getActiveDocumentContext()$path)
setwd()

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

# KNN class
#Xl el dataframe con los valores de aprendizaje del as x
#Xt el datafrmae con los x de testing
#k el parametro
#y las Y
accuracy=c()
sensibility=c()
specificity=c()
k=20
for (k in 1:5){
  yp = knn(xL, xT, yL, k=k, l=0, prob=T, use.all=T)
  ct = table(yp,yT);
  ct
  a=accu(yp,yT)
  b=sens(yp,yT)
  c=specif(yp,yT)
  accuracy<-c(accuracy,a)
  sensibility<-c(sensibility,b)
  specificity<-c(specificity,c)
}
k<-c(1,20)
resultado.data<-data.frame(k,accuracy,sensibility,specificity)
View(resultado.data)
dat <- read_csv("Resultados.csv")
write.csv(resultado.data,"Resultados.csv", row.names = FALSE)
yp
