import matplotlib.pyplot as plt

x_values = list(range(1,1001))
y_values = [x**2 for x in x_values]

#plt.scatter(x_values, y_values, s=45, edgecolor='none',c=(0,0,0.8))

#using a colormap
plt.scatter(x_values, y_values, s=45, edgecolor='none',c=y_values,cmap=plt.cm.Blues)



#set chart title and label axes.
plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)

#set size of tick labels.
plt.tick_params(axis='both', labelsize=14)

plt.axis([0,1100,0,1100000])

plt.show()