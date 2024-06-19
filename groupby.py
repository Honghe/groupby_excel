import polars as pl

df = pl.read_excel('demo.xlsx')
print(df)

# 合并第2至4列
df = df.with_columns(
    pl.concat_str(
        [
            pl.col("Value, A"),
            pl.col("Value\"\" B"), # xlsx转csv时，一个双引号转义为两个双引号
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