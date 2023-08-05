def plot_new_sample(df, x):

    X = df.iloc[:, 1:13]
    y = df["label"].replace({"Control": 0, "Covid": 1})  # .value_counts()
    x = x.values.reshape(1, -1)

    scaler = StandardScaler()
    scaler.fit(X.values)
    X = scaler.transform(X.values)

    means = np.array(
        [
            243.94969928,
            256.31424094,
            313.33404167,
            311.02738043,
            284.31009239,
            307.20553442,
            293.71868478,
            298.39285688,
            276.90539674,
            303.74205978,
            262.39199638,
            228.63297464,
        ]
    )
    vars = np.array(
        [
            32.38231873,
            15.39840351,
            0.30922943,
            0.11581567,
            14.18706441,
            0.67305964,
            2.09758948,
            0.96071839,
            7.81709395,
            1.53088058,
            4.84237249,
            13.75799395,
        ]
    )

    # means = scaler.mean_
    # vars = scaler.var_

    print("mean: ", means)
    print("var: ", vars)

    # X = scale_data(X.values, means=means,stds=vars **0.5)
    x = scale_data(x, means=means, stds=vars ** 0.5)

    print("scaled_new_data: ", x)

    pca = PCA(n_components=2)
    X = pca.fit_transform(X)

    # # print('Scaled X: ', X)

    print("before pca: ", x)
    x = pca.transform(x)
    print("after pca: ", x)

    # x = scaler.transform(x)
    # print(x)

    # pipe = Pipeline([
    #     ('scale', StandardScaler()),
    #     ('reduce_dims', PCA(n_components=2))])

    # pipe.fit(X.values)
    # X = pipe.transform(X.values)

    # print('pca_comp: ', x)

    group = y
    # group = y[:-10]
    cdict = {0: "blue", 1: "red"}
    class_label = {0: "Control", 1: "Covid"}

    scatter_x = X[:, 0]
    scatter_y = X[:, 1]

    fig, ax = plt.subplots()
    for g in np.unique(group):
        ix = np.where(group == g)
        ax.scatter(
            scatter_x[ix], scatter_y[ix], c=cdict[g], label=class_label[g], alpha=0.5
        )
    ax.scatter(x[:, 0], x[:, 1], c="black", label="new sample", s=70)
    ax.legend()
    ax.set_title("New data cluster assignment")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    # plt.show()
    fig.savefig("./static/img/sample_cluster.jpeg")
