from venn_diagram import plot_venn3

set1 = {'A', 'B', 'C', 'D', 'E'}
set2 = {'C', 'D', 'F', 'G'}
set3 = {'B', 'D', 'G', 'H', 'I', 'J'}

plot_venn3(set1, set2, set3,
           labels=['Set1', 'Set2', 'Set3'],
           colors=['#E41A1C', '#377EB8', '#FFAB52'],
           bold_labels=True,
           save_path="venn_final.png")
