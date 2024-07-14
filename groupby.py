import polars as pl

df = pl.read_excel('demo.xlsx')
print(df)

# 合并第2至4列
df = df.with_columns(
    pl.concat_str(
        [
            pl.col("Value, A"),
            pl.col("Value\" B"), # Polars 1.0版本“Change default engine for read_excel to "calamine"”，即默认不再转xlsx2csv再读取csv
            pl.col("Value C"),
        ],
        separator=", ",
    ).alias("concat"),
)
print(df)

# 按“Name”列groupby，对合并后的Cell内容使用换行符“\n”拼接
# https://stackoverflow.com/questions/75979059/python-polars-join-column-values-into-a-concatenated-string
df = df.group_by("Name").agg(pl.col("concat").str.concat('\n'))
print(df)

# 保存至xlsx
df.write_excel("output.xlsx", )