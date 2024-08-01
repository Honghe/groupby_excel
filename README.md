# Groupby excel table

Excel表格处理需求：按ID列将行合并，并使用换行符连接合并的行。

Polars与DuckDB是两个快速工具。

## Polars
Polars可直接读取xlsx文件。默认通过fastexcel使用Calamine库来读取xlsx。

```
df = pl.read_excel('demo.xlsx')
print(df)
```

使用`DataFrame.group_by()`:

```
df = pl.DataFrame(
    {
        "a": ["a", "b", "a", "b", "c"],
        "b": [1, 2, 1, 3, 3],
        "c": [5, 4, 3, 2, 1],
    }
)
df.group_by("a").agg(pl.col("b").sum())
shape: (3, 2)
┌─────┬─────┐
│ a   ┆ b   │
│ --- ┆ --- │
│ str ┆ i64 │
╞═════╪═════╡
│ a   ┆ 2   │
│ b   ┆ 5   │
│ c   ┆ 3   │
└─────┴─────┘
```
### 效果

```python
import polars as pl

df = pl.read_excel('demo.xlsx')
```

```
shape: (4, 4)
┌───────┬──────────┬───────────┬─────────┐
│ Name  ┆ Value, A ┆ Value"" B ┆ Value C │
│ ---   ┆ ---      ┆ ---       ┆ ---     │
│ str   ┆ str      ┆ str       ┆ str     │
╞═══════╪══════════╪═══════════╪═════════╡
│ Bob   ┆ Book     ┆ Chair     ┆ 一      │
│ Bob   ┆ Zebra    ┆ 二        ┆ 三      │
│ Sally ┆ 四       ┆ Tablet    ┆ 五      │
│ Sally ┆ 六       ┆ 七        ┆ Vanilla │
└───────┴──────────┴───────────┴─────────┘
```

```python
df = df.with_columns(
    pl.concat_str(
        [
            pl.col("Value, A"),
            pl.col("Value\"\" B"), 
            pl.col("Value C"),
        ],
        separator=", ",
    ).alias("concat"),
)
```

```
shape: (4, 5)
┌───────┬──────────┬───────────┬─────────┬─────────────────┐
│ Name  ┆ Value, A ┆ Value"" B ┆ Value C ┆ concat          │
│ ---   ┆ ---      ┆ ---       ┆ ---     ┆ ---             │
│ str   ┆ str      ┆ str       ┆ str     ┆ str             │
╞═══════╪══════════╪═══════════╪═════════╪═════════════════╡
│ Bob   ┆ Book     ┆ Chair     ┆ 一      ┆ Book, Chair, 一 │
│ Bob   ┆ Zebra    ┆ 二        ┆ 三      ┆ Zebra, 二, 三   │
│ Sally ┆ 四       ┆ Tablet    ┆ 五      ┆ 四, Tablet, 五  │
│ Sally ┆ 六       ┆ 七        ┆ Vanilla ┆ 六, 七, Vanilla │
└───────┴──────────┴───────────┴─────────┴─────────────────┘
```

```python
df = df.group_by("Name").agg(pl.col("concat").str.concat('\n'))
```

```
shape: (2, 2)
┌───────┬─────────────────┐
│ Name  ┆ concat          │
│ ---   ┆ ---             │
│ str   ┆ str             │
╞═══════╪═════════════════╡
│ Bob   ┆ Book, Chair, 一 │
│       ┆ Zebra, 二, 三   │
│ Sally ┆ 四, Tablet, 五  │
│       ┆ 六, 七, Vanilla │
└───────┴─────────────────┘
```

## DuckDB
步骤如下：
1. 将excel导出为csv；
2. 将csv转化为UTF8（duckdb使得UTF8，但Excel导出的csv为ANSI，中文乱码）；
3. 先将B之后的列合并为一列（Excel中可以使用“&”等）；
4. 使用`string_agg`来按id列将行合并；
5. 使用copy导出为excel

```sql
copy (SELECT Name, string_agg("Value, A", ', ' order by Name desc) AS countdown from "Book1.csv" group by Name) 
to 'output.xlsx' 
with (format gdal, driver 'xlsx');
```

## Background
2023.12.05, Microsoft 365 announces the availability of two new functions in Excel: GROUPBY and PIVOTBY.
https://insider.microsoft365.com/en-us/blog/new-aggregation-functions-in-excel-groupby-and-pivotby