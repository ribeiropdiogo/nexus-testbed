# Read the input data
input_file <- file.path(getwd(), "data/heterogeneous.csv")
df <- read.csv(input_file)

# Set the desired order of algorithms
df$Algorithm <- factor(df$Algorithm, levels = c("TruthFinder", "CRH", "Nexus"))

# Define the output file
output_file <- file.path(getwd(), "pdf/boxplot-heterogeneous.pdf")
pdf(output_file)

# Set the margins: mar = c(bottom, left, top, right)
par(mar = c(6.5, 6.5, 2, 1))
# Set the margins: mgp
par(mgp = c(4.25, 1.75, 0))

# Build the plot
boxplot(
  df$Accuracy ~ df$Algorithm,
  ylab = "Accuracy (%)",           # Y axis label
  xlab = "Algorithm",          # X axis label
  outline = FALSE,             # Show outliers
  lwd = 3,                     # Line width
  cex.lab = 3,                 # Axis label size
  cex.axis = 2.25,              # Axis text size
  boxwex = 0.5                 # Increase box width
)

box(
  lwd = 4        # Change the width of the outside box
)  

dev.off()