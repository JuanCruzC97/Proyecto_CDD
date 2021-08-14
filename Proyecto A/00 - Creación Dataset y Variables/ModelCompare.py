import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve, classification_report

# Creamos una clase modelCompare que permite ir construyendo un dataset con los modelos utilizados y calcular sus métricas
# Permite comparar de manera más acotada o resumida los modelos entrenados.

# HACER:
## Agregar otra clase para cubrir problema Regresion/Clasificacion.
class modelCompareClass:

    # Al crearse una instancia de la clase se genera el siguiente dataset vacío.
    def __init__(self):
        columnas = ['Model', 'Train Accuracy', 'Test Accuracy', 'Train Sen', 'Test Sen', 'Train Spec', 'Test Spec', 'Train AUC', 'Test AUC']
        self.results = pd.DataFrame(columns = columnas)

    # Este método realiza todos los cálculos de las métricas de clasificación.
    # Devuelve un diccionario con las métricas.
    def __metricsCalculation(self, model, X_train, y_train, X_test, y_test, probas = True):
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        # Incluímos el argumento probas para poder usar la comparación en modelos sin el método predict_proba.
        if probas == True:
            y_train_pred_proba = model.predict_proba(X_train)[:,1]
            y_test_pred_proba = model.predict_proba(X_test)[:,1]

        acc_train = accuracy_score(y_train, y_train_pred)
        acc_test = accuracy_score(y_test, y_test_pred)

        conf_train = confusion_matrix(y_train, y_train_pred)
        sen_train = conf_train[1,1]/(conf_train[1,1]+conf_train[1,0])
        spec_train = conf_train[0,0]/(conf_train[0,0]+conf_train[0,1])

        conf_test = confusion_matrix(y_test, y_test_pred)
        sen_test = conf_test[1,1]/(conf_test[1,1]+conf_test[1,0])
        spec_test = conf_test[0,0]/(conf_test[0,0]+conf_test[0,1])

        if probas == True:
            auc_train = roc_auc_score(y_train, y_train_pred_proba)
            auc_test = roc_auc_score(y_test, y_test_pred_proba)

        metrics = {
            'Acc_Train':acc_train,
            'Acc_Test':acc_test,
            'Sen_Train':sen_train,
            'Sen_Test':sen_test,
            'Spec_Train':spec_train,
            'Spec_Test':spec_test,
            'AUC_Train':np.NaN,
            'AUC_Test':np.NaN,
            'Conf_Train':conf_train,
            'Conf_Test':conf_test
        }

        if probas == True:
            metrics['AUC_Train'] = auc_train
            metrics['AUC_Test'] = auc_test

        return metrics

    # El metodo addModel permite agregar un modelo al dataframe de comparacion.
    # Se incluyen los datasets utilizados permitiendo evaluar modelos con distintas variables X.
    def addModel(self, name, model, X_train, y_train, X_test, y_test, probas = True):
        metrics = self.__metricsCalculation(model, X_train, y_train, X_test, y_test, probas=probas)

        self.results.loc[self.results.shape[0]] = [
            name,
            metrics['Acc_Train'],
            metrics['Acc_Test'],
            metrics['Sen_Train'],
            metrics['Sen_Test'],
            metrics['Spec_Train'],
            metrics['Spec_Test'],
            metrics['AUC_Train'],
            metrics['AUC_Test']
        ]

    # Este método permite eliminar un modelo del dataframe results.
    def dropModel(self, index):
        self.results = self.results.drop(index)
        self.results.reset_index(drop=True, inplace=True)

    # plotAccuracy permite graficar de manera rápida el valor de Accuracy de Train y Test.
    # Ordena los modelos según el Accuracy Test.
    def plotAccuracy(self, ylim = [0,1]):
        df_plot = self.results.sort_values('Test Accuracy', ascending = False)

        plt.plot(df_plot['Model'], df_plot['Train Accuracy'])
        plt.plot(df_plot['Model'], df_plot['Test Accuracy'], color = 'red')
        plt.scatter(df_plot['Model'], df_plot['Train Accuracy'])
        plt.scatter(df_plot['Model'], df_plot['Test Accuracy'], color = 'red')
        plt.title('Accuracy Train and Test')
        plt.xlabel('Model')
        plt.ylabel('Accuracy')
        plt.xticks(rotation = 45)
        plt.legend(['Train', 'Test'], loc = 'lower right')
        plt.ylim(ylim)
        plt.show()


    # Este método permite obtener un resumen de Train y Test Metrics para un modelo de Clasificación.
    ### Se puede agregar un argumento para hacer addModel directamente.
    def modelReportClass(self, name, model, X_train, y_train, X_test, y_test, heatmap = True, ROC = True, classReport = False, addModel = False, probas = True):
        metrics = self.__metricsCalculation(model, X_train, y_train, X_test, y_test, probas = probas)

        print(f'------------{name}------------\n')
        print(f'---------Train Metrics-----------')
        print(f'Accuracy = {metrics["Acc_Train"]}')
        print(f'Sensibility = {metrics["Sen_Train"]}')
        print(f'Specificity = {metrics["Spec_Train"]}')
        if probas == True:
            print(f'AUC = {metrics["AUC_Train"]}\n')
        print(f'Confusion Matrix')
        print(metrics['Conf_Train'])
        print('-----------------------------------')
        print('\n')
        print(f'-----------Test Metrics-----------')
        print(f'Accuracy = {metrics["Acc_Test"]}')
        print(f'Sensibility = {metrics["Sen_Test"]}')
        print(f'Specificity = {metrics["Spec_Test"]}')
        if probas == True:
            print(f'AUC = {metrics["AUC_Test"]}\n')
        print(f'Confusion Matrix')
        print(metrics['Conf_Test'])
        if heatmap == True:
            sns.heatmap(metrics['Conf_Test'], annot=True, annot_kws={"size": 10}, cmap="YlGnBu",fmt='g', linewidths = 1, linecolor = 'black')
            plt.title(f'{name} Confusion Matrix Heatmap')
            plt .xlabel('Predictions')
            plt.ylabel('Observations')
            plt.show()
        if ROC == True:
            fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:,1])
            plt.plot([0,1], [0,1], 'k--')
            plt.plot(fpr, tpr, label = name)
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title(f'{name} ROC Curve')
            plt.show()
        if classReport == True:
            print(f'{name} Test Classification Report')
            print(classification_report(y_test, model.predict(X_test)))

        if addModel == True:
            self.addModel(self, name, model, X_train, y_train, X_test, y_test, probas=probas)
