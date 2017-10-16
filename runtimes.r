library(fitdistrplus)


fileUri = "C:/Users/Tom/Documents/Computing Science/ADS/rawdata/runtimes.csv"
input <- read.csv(file=fileUri,head=TRUE,sep=";")

col <- input$Stadscentrum

fw <- fitdist(col, "gamma")
#summary(fw)

fg <- fitdist(col, "gamma")
fln <- fitdist(col, "lnorm")
fn <- fitdist(col, "norm")
fb <- fitdist(col, "weibull")
#par(mfrow = c(2, 2))
plot.legend <- c("lognormal", "gamma", "normal", "weibull")
#denscomp(list(fln, fg, fn, fb), legendtext = plot.legend)
#qqcomp(list(fln, fg, fn, fb), legendtext = plot.legend)
#cdfcomp(list(fln, fg, fn, fb), legendtext = plot.legend)
#ppcomp(list(fln, fg, fn, fb), legendtext = plot.legend)

gofstat(list(fg, fln, fn, fb), fitnames = c("lognormal", "gamma", "normal", "weibull"))

df = data.frame(nrow = 4, ncol = 14)

for(i in colnames(input)){
  print(i)
  
}
