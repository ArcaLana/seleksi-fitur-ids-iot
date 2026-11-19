"""Kode 9.3  Peringkat fitur dengan metode embedded dan wrapper
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.feature_selection import RFE
from xgboost import XGBClassifier
 
def xgb():
    return XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=100,
                         tree_method="hist", n_jobs=2, random_state=SEED, verbosity=0)
 
rank["rf_imp"]  = np.argsort(-RandomForestClassifier(n_estimators=100, n_jobs=2,
                  random_state=SEED).fit(Xtr, ytr).feature_importances_)
rank["xgb_imp"] = np.argsort(-xgb().fit(Xtr, ytr).feature_importances_)
 
i1, i2 = train_test_split(np.arange(len(Xtr)), test_size=0.2, stratify=ytr, random_state=SEED)
mv = xgb().fit(Xtr[i1], ytr[i1])                              # validasi dari data latih saja
pi = permutation_importance(mv, Xtr[i2[:8000]], ytr[i2[:8000]], n_repeats=3,
                            random_state=SEED, scoring="f1_macro")
rank["perm"] = np.argsort(-pi.importances_mean)
 
sc = StandardScaler().fit(Xtr[sub])
l1 = LogisticRegression(penalty="l1", solver="saga", C=0.05, max_iter=150, tol=1e-3)
l1.fit(sc.transform(Xtr[sub]), ytr[sub])
rank["l1"] = np.argsort(-np.abs(l1.coef_).max(axis=0))
 
s30, _ = train_test_split(np.arange(len(Xtr)), train_size=30000, stratify=ytr, random_state=SEED)
rfe = RFE(XGBClassifier(learning_rate=0.1, max_depth=4, n_estimators=40, tree_method="hist",
          n_jobs=2, random_state=SEED, verbosity=0), n_features_to_select=5, step=5)
rfe.fit(Xtr[s30], ytr[s30]); rank["rfe_xgb"] = np.argsort(rfe.ranking_)
