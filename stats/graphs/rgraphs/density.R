# Read the input data
input_file <- file.path(getwd(), "data/data.csv")
df <- read.csv(input_file)

# Define the output file
output_file <- file.path(getwd(), "pdf/density-nexus-all.pdf")
pdf(output_file)

# Set the margins: mar = c(bottom, left, top, right)
par(mar = c(6, 6, 2, 2.2))
# Set the margins: mgp
par(mgp = c(4, 1.5, 0))
# No extra padding on axes
par(xaxs = "i", yaxs = "i")

# Filter the data
filtered_data <- df[df$Algorithm == "Nexus", ]
# Compute the density
d <- density(filtered_data$Accuracy)
# Normalize y values so the max is 1
d$y <- d$y / max(d$y)

# Build the plot
plot(
  d,
  main = "",
  xlab = "Accuracy (%)",
  ylab = "Density",
  ylim = c(0, 1),      # Define y limit  
  xlim = c(99.2, 100),      # Define x limit
  lwd = 4,             # Line width
  cex.lab = 2.5,       # Axis label size
  cex.axis = 2,        # Axis text size
)

# Fill under the curve with gray color (semi-transparent)
polygon(c(d$x[1], d$x, d$x[length(d$x)]), 
        c(0, d$y, 0), 
        col = gray(0.7), border = NA)

# Add the density line on top
lines(d, col = "black", lwd = 2)

box(
  lwd = 3        # Change the width of the outside box
)  

dev.off()