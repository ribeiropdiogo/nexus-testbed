# Define the output file
output_file <- file.path(getwd(), "pdf/linegraph-heterogeneous-dc.pdf")
pdf(output_file)

# Set the margins: mar = c(bottom, left, top, right)
par(mar = c(6, 7, 2, 1))
# Set the margins: mgp
par(mgp = c(4.5, 1.5, 0))

# Define x-axis points
xaxis=c(20,40,60,80)

# Define points
tf_het=c(16.67,35.00,58.33,82.22)
crh_het=c(8.33,16.67,8.33,22.22)
nexus_het=c(0,0,0,2.22)


plot( tf_het~xaxis,
      type="o", bty="o",
      xlab="Noise (%)",
      ylab="Incorrect Results (%)",
      col="black",
      lwd=5, pch=17, cex=3,
      ylim=c(0,100),
      cex.lab = 3,
      cex.axis = 2.5
    )

lines(crh_het ~xaxis,   col="black", lwd=5, cex=3, pch=16, type="o")
lines(nexus_het ~xaxis, col="black", lwd=5, cex=3, pch=15, type="o")

# Add a legend
legend("topleft", 
       legend = c("TruthFinder", "CRH", "Nexus"), 
       col = c(
         "black", 
         "black", 
         "black"
        ), 
       lwd = 5,
       pch = c(17,16,15), 
       bty = "n", 
       pt.cex = 3.5, 
       cex = 2.25, 
       text.col = "black", 
       horiz = F , 
       inset = c(0.05, 0.05))

box(lwd = 4)

dev.off()