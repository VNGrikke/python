import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="ticks")

tips = sns.load_dataset("tips")
taxis = sns.load_dataset("taxis")
diamonds = sns.load_dataset("diamonds")
dots = sns.load_dataset("dots")
plt.figure(figsize=(12, 6))

# KDE plot một biến
sns.scatterplot(data=dots, x="choice", y="time", hue="time")

plt.title("Scatter plot của Dots")
plt.show()
