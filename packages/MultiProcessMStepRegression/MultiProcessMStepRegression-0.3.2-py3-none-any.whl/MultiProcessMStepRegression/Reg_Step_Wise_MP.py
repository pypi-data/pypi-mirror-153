# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 14:53:31 2020

@author: 王文皓(wangwenhao)
"""

from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod.families import Binomial
from statsmodels.genmod.families.links import logit
import statsmodels.api as sm
from .Reg_Sup_Step_Wise_MP import Regression

class LogisticReg(Regression):

    def __init__(self,X,y,given_cols=[],fit_weight=None,measure='ks',measure_weight=None,measure_frac=None,measure_X=None,measure_y=None,kw_measure_args=None,max_pvalue_limit=0.05,max_vif_limit=3,max_corr_limit=0.6,coef_sign=None,iter_num=20,kw_algorithm_class_args=None,n_core=None,logger_file_CH=None,logger_file_EN=None):
        Regression.__init__(self,X=X,y=y,given_cols=given_cols,fit_weight=fit_weight,measure=measure,measure_weight=measure_weight,measure_frac=measure_frac,measure_X=measure_X,measure_y=measure_y,kw_measure_args=kw_measure_args,max_pvalue_limit=max_pvalue_limit,max_vif_limit=max_vif_limit,max_corr_limit=max_corr_limit,coef_sign=coef_sign,iter_num=iter_num,kw_algorithm_class_args=kw_algorithm_class_args,n_core=n_core,logger_file_CH=logger_file_CH,logger_file_EN=logger_file_EN)
        
    def _regression(self,in_vars):
        X = self.X[in_vars]
        if self.fit_weight is None:
            if self.kw_algorithm_class_args is not None:
                glm = GLM(self.y,sm.add_constant(X),family = Binomial(link=logit),**self.kw_algorithm_class_args)
            else:
                glm = GLM(self.y,sm.add_constant(X),family = Binomial(link=logit))
        else:
            if self.kw_algorithm_class_args is not None:
                glm = GLM(self.y,sm.add_constant(X),family = Binomial(link=logit),freq_weights = self.fit_weight,**self.kw_algorithm_class_args)
            else:
                glm = GLM(self.y,sm.add_constant(X),family = Binomial(link=logit),freq_weights = self.fit_weight)         
        clf = glm.fit()      
        clf.intercept_=[clf.params.const]
        clf.coef_=[clf.params[1:]]
        return clf

class LinearReg(Regression):

    def __init__(self,X,y,given_cols=[],fit_weight=None,measure='r2',measure_weight=None,measure_X=None,measure_y=None,kw_measure_args=None,max_pvalue_limit=0.05,max_vif_limit=3,max_corr_limit=0.6,coef_sign=None,iter_num=20,kw_algorithm_class_args=None,n_core=None,logger_file_CH=None,logger_file_EN=None):
        Regression.__init__(self,X=X,y=y,given_cols=given_cols,fit_weight=fit_weight,measure=measure,measure_weight=measure_weight,measure_X=measure_X,measure_y=measure_y,kw_measure_args=kw_measure_args,max_pvalue_limit=max_pvalue_limit,max_vif_limit=max_vif_limit,max_corr_limit=max_corr_limit,coef_sign=coef_sign,iter_num=iter_num,kw_algorithm_class_args=kw_algorithm_class_args,n_core=n_core,logger_file_CH=logger_file_CH,logger_file_EN=logger_file_EN)
            
    def _regression(self,in_vars):
        X = self.X[in_vars]
        if self.fit_weight is None:
            if self.kw_algorithm_class_args is not None:
                reg = sm.OLS(self.y,sm.add_constant(X),**self.kw_algorithm_class_args)
            else:
                reg = sm.OLS(self.y,sm.add_constant(X))
        else:
            if self.kw_algorithm_class_args is not None:
                reg = sm.WLS(self.y,sm.add_constant(X),weights=self.fit_weight,**self.kw_algorithm_class_args)
            else:
                reg = sm.WLS(self.y,sm.add_constant(X),weights=self.fit_weight)       
        clf = reg.fit()      
        clf.intercept_=[clf.params.const]
        clf.coef_=[clf.params[1:]]
        return clf