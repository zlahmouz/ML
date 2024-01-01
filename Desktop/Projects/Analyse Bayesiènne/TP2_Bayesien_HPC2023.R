#Correction TP2 HPC - BigData : algorithme de Metropolis-Hastings

sig2=1 ; d2=10 ; b=5 ; n=5 
y=c(9.37,10.18,9.16,11.6,10.33)

#posterior : N(mu,s2)
mu=(b/d2+sum(y)/sig2)/(1/d2+n/sig2)
s2=1/(1/d2+n/sig2)
mu ; s2

#Algorithme Metropolis avec distribution de transition gaussienne

chaine=function(delta2,S){
theta=0;f=0;THETA=0
for (i in 1:S) {
	theta.star=rnorm(1,theta,sqrt(delta2))
	log.r=sum(dnorm(y,theta.star,sqrt(sig2),log=T))+
	     dnorm(theta.star,b,sqrt(d2),log=T)-
	     sum(dnorm(y,theta,sqrt(sig2),log=T))-
	     dnorm(theta,b,sqrt(d2),log=T)

	if (log(runif(1))<log.r) {
		theta=theta.star
		f=f+1 
		}
	THETA=c(THETA,theta)
	}
# Frequence d'acceptation
print(paste("Frequence d'acceptation =",f/S))
return(THETA)
}

THETA2=chaine(2,10000)

hist(THETA2[50:10000],prob=T)
x=seq(8,12,0.01)
lines(x,dnorm(x,mu,sqrt(s2)))

x11()
par(mfrow=c(2,1))
plot(THETA2,type="l")
plot(THETA2[1:400],type="l")

THETA64=chaine(64,10000)
THETAinv32=chaine(1/32,10000)

x11()
plot(THETA2[1:400],ylab=expression(theta),type="l",lwd=3)
lines(THETA64[1:400],col="red",lwd=3)
lines(THETAinv32[1:400],col="blue",lwd=3)
legend(300,2,legend=c("Delta2=64","Delta2=2","Delta2=1/32"),text.col=c("red","black","blue"),bty="n")


x11()
par(mfrow=c(1,3))
acf(THETAinv32) ; acf(THETA2) ; acf(THETA64) 

#impact periode de chauffe sur les estimations des moments mu et s2 :

mean(THETAinv32)
mean(THETAinv32[200:10000])
var(THETAinv32)
var(THETAinv32[200:10000])



#####################################################################


#Algorithme Metropolis avec distribution de transition uniforme

chaine2=function(delta,S){
theta=0;f=0;THETA=0
for (i in 1:S) {
	theta.star=runif(1,theta-delta,theta+delta)
	log.r=sum(dnorm(y,theta.star,sqrt(sig2),log=T))+
	     dnorm(theta.star,b,sqrt(d2),log=T)-
	     sum(dnorm(y,theta,sqrt(sig2),log=T))-
	     dnorm(theta,b,sqrt(d2),log=T)

	if (log(runif(1))<log.r) {
		theta=theta.star
		f=f+1 
		}
	THETA=c(THETA,theta)
	}
# Frequence d'acceptation
print(paste("Frequence d'acceptation =",f/S))
return(THETA)
}

THETAU1=chaine2(1,10000)

hist(THETAU1[100:10000],prob=T)
x=seq(8,12,0.01)
lines(x,dnorm(x,mu,sqrt(s2)))

x11()
par(mfrow=c(2,1))
plot(THETAU1,type="l")
plot(THETAU1[1:400],type="l")

THETAU100=chaine2(100,10000)
THETAUinv10=chaine2(1/10,10000)

x11()
plot(THETAU1[1:1500],ylab=expression(theta),type="l",lwd=3)
lines(THETAU100[1:1500],col="red",lwd=3)
lines(THETAUinv10[1:1500],col="blue",lwd=3)
legend(750,2,legend=c("Delta=100","Delta=1","Delta=1/10"),text.col=c("red","black","blue"),bty="n")

x11()
par(mfrow=c(1,3))
acf(THETAUinv10) ; acf(THETAU1) ; acf(THETAU100)


#impact periode de chauffe sur les estimations des moments mu et s2 :

mean(THETAUinv10)
mean(THETAUinv10[1000:10000])
var(THETAUinv10)
var(THETAUinv10[1000:10000])



