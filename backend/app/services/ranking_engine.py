def single_rank(
    df,
    metric,
    ascending=False
):

    return df.sort_values(
        by=metric,
        ascending=ascending
    )

def multi_rank(df, metrics):

    sort_columns = []

    ascending = []

    for metric in metrics:

        sort_columns.append(
            metric["name"]
        )

        ascending.append(
            metric["ascending"]
        )

    return df.sort_values(
        by=sort_columns,
        ascending=ascending
    )

def composite_rank(
    df,
    metrics
):

    rank_columns = []

    for metric in metrics:

        col_name = (
            metric["name"] +
            "_rank"
        )

        df[col_name] = df[
            metric["name"]
        ].rank(
            ascending=metric[
                "ascending"
            ]
        )

        rank_columns.append(
            col_name
        )

    df["final_rank"] = (
        df[rank_columns]
        .mean(axis=1)
    )

    return df.sort_values(
        "final_rank"
    )