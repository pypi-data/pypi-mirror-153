import matplotlib.pyplot as plt

def boxplot( boxplot_data, title, x_label, y_label, xtick_labels, output_file ):
  # matplotlib比较old， 输入是 二维list
  fig = plt.figure(1, figsize=(12, 7))
  ax = fig.add_subplot(111)
  bp = ax.boxplot(boxplot_data, patch_artist=True)

  for box in bp['boxes']:
    box.set(facecolor='#087E8B', alpha=0.6, linewidth=2)

  for whisker in bp['whiskers']:
    whisker.set(linewidth=2)

  for median in bp['medians']:
    median.set(color='black', linewidth=3)

  ax.set_title( title )
  ax.set_xlabel( x_label)
  ax.set_ylabel( y_label )
  ax.set_xticklabels( xtick_labels )
  fig.savefig(output_file)
  fig.close()

def scatterplot( x_list, y_list, title, x_label, y_label, text, output_file ):
  fig = plt.figure(figsize=(12, 7))
  ax = plt.gca()
  plt.scatter(x=x_list, y=y_list)
  plt.text(0.5, 0.75, text, transform = ax.transAxes)
  plt.title( title )
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  fig.savefig(output_file)
  fig.close()
