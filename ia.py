import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import json
# Load and process the data
with open('data_clasified(1).json', 'r') as file:
    data = json.load(file)

tickets = data['tickets_emitidos']
features_list = []

for ticket in tickets:
    cliente = ticket['cliente']
    fecha_apertura = datetime.strptime(ticket['fecha_apertura'], '%Y-%m-%d')
    fecha_cierre = datetime.strptime(ticket['fecha_cierre'], '%Y-%m-%d')
    duracion_ticket = (fecha_cierre - fecha_apertura).days
    es_mantenimiento = ticket['es_mantenimiento']
    satisfaccion_cliente = ticket['satisfaccion_cliente']
    tipo_incidencia = ticket['tipo_incidencia']
    es_critico = ticket['es_critico']
    contactos = ticket['contactos_con_empleados']
    num_contactos = len(contactos)
    tiempo_total_contactos = sum(contacto['tiempo'] for contacto in contactos)

    features = {
        'cliente': cliente,
        'duracion_ticket': duracion_ticket,
        'es_mantenimiento': es_mantenimiento,
        'satisfaccion_cliente': satisfaccion_cliente,
        'tipo_incidencia': tipo_incidencia,
        'num_contactos': num_contactos,
        'tiempo_total_contactos': tiempo_total_contactos,
        'es_critico': es_critico
    }
    features_list.append(features)

# Create DataFrame and encode categorical variables
df = pd.DataFrame(features_list)
df_encoded = pd.get_dummies(df, columns=['cliente', 'tipo_incidencia'])
df_encoded['es_critico'] = df_encoded['es_critico'].astype(int)

# Split features and target
X = df_encoded.drop('es_critico', axis=1)
y = df_encoded['es_critico']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Logistic Regression
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train, y_train)
y_pred_log_reg = log_reg.predict(X_test)
accuracy_log_reg = accuracy_score(y_test, y_pred_log_reg)
print(f'Accuracy de Regresión Logística: {accuracy_log_reg}')

# Visualize Logistic Regression coefficients
plt.figure(figsize=(10, 6))
plt.bar(X.columns, log_reg.coef_[0])
plt.xticks(rotation=90)
plt.title('Importancia de las Características - Regresión Logística')
plt.tight_layout()
plt.savefig('log_reg_coefficients.png')
plt.close()

# Train Decision Tree
tree_clf = DecisionTreeClassifier(random_state=42)
tree_clf.fit(X_train, y_train)
y_pred_tree = tree_clf.predict(X_test)
accuracy_tree = accuracy_score(y_test, y_pred_tree)
print(f'Accuracy de Árbol de Decisión: {accuracy_tree}')

# Visualize Decision Tree
plt.figure(figsize=(20, 10))
plot_tree(tree_clf, feature_names=X.columns, class_names=['No Crítico', 'Crítico'], filled=True)
plt.savefig('decision_tree.png')
plt.close()

# Train Random Forest
rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train, y_train)
y_pred_rf = rf_clf.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f'Accuracy de Bosque Aleatorio: {accuracy_rf}')

# Visualize Random Forest feature importance
importances = rf_clf.feature_importances_
forest_importances = pd.Series(importances, index=X.columns)
plt.figure(figsize=(10, 6))
forest_importances.plot.bar()
plt.title('Importancia de las Características - Bosque Aleatorio')
plt.tight_layout()
plt.savefig('random_forest_importance.png')
plt.close()


# Prediction function
def predecir(ticket_data, modelo):
    new_ticket = {
        'duracion_ticket': ticket_data['duracion_ticket'],
        'es_mantenimiento': 1 if ticket_data['es_mantenimiento'] else 0,
        'satisfaccion_cliente': ticket_data['satisfaccion_cliente'],
        'num_contactos': ticket_data['num_contactos'],
        'tiempo_total_contactos': ticket_data['tiempo_total_contactos'],
    }
    for col in X.columns:
        if col.startswith('cliente_'):
            new_ticket[col] = 1 if col == f'cliente_{ticket_data["cliente"]}' else 0
        elif col.startswith('tipo_incidencia_'):
            new_ticket[col] = 1 if col == f'tipo_incidencia_{ticket_data["tipo_incidencia"]}' else 0

    new_ticket_df = pd.DataFrame([new_ticket], columns=X.columns).fillna(0)

    if modelo == 'log_reg':
        prediccion = log_reg.predict(new_ticket_df)[0]
    elif modelo == 'tree':
        prediccion = tree_clf.predict(new_ticket_df)[0]
    elif modelo == 'rf':
        prediccion = rf_clf.predict(new_ticket_df)[0]
    else:
        raise ValueError("Modelo no válido")

    return 'Crítico' if prediccion == 1 else 'No Crítico'
