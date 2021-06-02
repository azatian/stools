from Bio import SeqIO
import os.path
import pandas as pd
import plotly.graph_objects as go

def loader(in_file):
    if os.path.isfile(in_file):
        df = pd.DataFrame(columns=["Scaffold", "Length", "SubScaffolds", "LengthofSubScaffolds"])
        record_dict = SeqIO.to_dict(SeqIO.parse(in_file, "fasta"))
        df = data_wrangle(df, record_dict)
        odirectory = os.path.dirname(in_file) + "/meta"
        if not os.path.exists(odirectory):
            os.makedirs(odirectory)
        save_csv(df, odirectory+"/final_fasta_meta.csv")
        save_fig(df, odirectory+"/final_fasta_meta.png")
        print("DONE")
        return
    else:
        print("ERROR: Fafsa file does not exist!")

def data_wrangle(df, record_dict):
    for key in record_dict:
        get_subscaff = record_dict[key].description.split(record_dict[key].name + " ")[1].split(",")
        df = df.append({"Scaffold": record_dict[key].name  , "Length" : len(record_dict[key]), "SubScaffolds" : get_subscaff, "LengthofSubScaffolds" : len(get_subscaff) }, ignore_index=True)
    
    if len(df) > 0:
        return df
    
    else:
        print("DEBUG: DataFrame Empty, no outputs returned")

def save_csv(df, odirectory):
    df.to_csv(odirectory, encoding="utf-8", index=False)

def save_fig(df, odirectory):
    df_sort = df.sort_values(by=["LengthofSubScaffolds"], ascending=False)
    fig = go.Figure(data=go.Scatter(x=df_sort["Scaffold"],y=df_sort["LengthofSubScaffolds"], mode='markers', connectgaps=False))
    fig.update_layout(title='Super Scaffold Components',
                   xaxis_title='Index',
                   yaxis_title='Count')
    fig.write_image(odirectory, width=1400, height=1000)