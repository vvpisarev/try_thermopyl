
import thermopyl as th
from thermopyl import thermoml_lib
import cirpy
import numpy as np
import pandas as pd
import functools
df = th.pandas_dataframe(
)
from joblib import Memory
mem = Memory(location="/home/grigory/.thermoml/")
@mem.cache
def resolve_cached(x, rtype):
   return cirpy.resolve(x, rtype)

dt = list(df.columns)
experiments=["Mass density, kg/m3"]
ind = reduce(lambda x, y: x.union(y), ind_list)
ind_list = [df[exp].dropna().index for exp in experiments]
ind = reduce(lambda x, y: x.union(y), ind_list)
ind = functools.reduce(lambda x, y: x.union(y), ind_list)
df = df.iloc[ind]
name_to_formula = pd.read_parquet("~/.thermoml/compound_name_to_formula.pq")
name_to_formula = name_to_formula.dropna()
df["n_components"] = df.components.apply(
    lambda x: len(x.split("__"))
)
df = df[df.n_components == 1]
df.dropna(axis=1, how='all', inplace=True)
df = df[df['phase'] == 'Liquid']
df = df[df.components.isin(name_to_formula.index)]
df["formula"] = df.components.apply(lambda chemical: name_to_formula.loc[chemical])
heavy_atoms = [ "C" ]
c_atoms = [ "C" ]  
desired_atoms = ["H"] + heavy_atoms

df["n_atoms"] = df.formula.apply(
    lambda formula_string: thermoml_lib.count_atoms(formula_string))
df["n_heavy_atoms"] = df.formula.apply(
    lambda formula_string: thermoml_lib.count_atoms_in_set(
        formula_string, heavy_atoms))
df["n_c_atoms"] = df.formula.apply(
    lambda formula_string: thermoml_lib.count_atoms_in_set(
        formula_string, c_atoms))        
df["n_desired_atoms"] = df.formula.apply(
    lambda formula_string: thermoml_lib.count_atoms_in_set(
        formula_string, desired_atoms))
df["n_other_atoms"] = df.n_atoms - df.n_desired_atoms  # how many undesired atoms are in each row?
df = df[df.n_other_atoms ==
        0]  # get rid of rows with other atoms other than those desired
df = df[df.n_heavy_atoms > 0]
df = df[df.n_c_atoms > 0]
df = df[df.n_heavy_atoms <= 20]
df.dropna(axis=1, how='all', inplace=True)

df["cas"] = df.components.apply(lambda x: thermoml_lib.get_first_entry(
    resolve_cached(x, "cas")))
df["smiles"] = df.components.apply(lambda x: resolve_cached(x, "smiles"))  # This should be cached via sklearn.    
keep=df[df['Pressure, kPa'] > 120.].cas
df=df[df.cas.isin(keep)]
df=df[df.smiles.apply(lambda x: bool(re.match('^[C]+$',x)))]
dfbig = pd.concat([
    df['filename'], df["components"],df["smiles"],
    df["Temperature, K"], df["Pressure, kPa"], 
    df["Mass density, kg/m3"],
],
                  axis=1,
                  keys=[
                      "filename", "components","smiles"
                      "Temperature, K", "Pressure, kPa", "Mass density, kg/m3",                   
                  ])
dfbig.to_csv("./density.csv",sep=';')

