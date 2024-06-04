#coding=utf-8
from abc import ABCMeta, abstractmethod
import os

class BasePrintForm(object):
    __metaclass__ = ABCMeta

    def __init__(self, params):
        self.params = params

    @abstractmethod
    def print_(self):
        pass

    @abstractmethod
    def preview(self):
        pass



class FRPrintForm(BasePrintForm):
    def __init__(self, fr3, params, env):
        BasePrintForm.__init__(self, params)
        self.env = env
        self.params[u'ConnectionString'] = self.get_connection_string()

        import win32com.client
        self.fr = win32com.client.Dispatch(u'FastReport.TfrxReport')

        self.fr.LoadReportFromFile(os.path.join(self.env.config.paths.rpt, fr3))
        self.set_parameters()

    def get_connection_string(self):
        dbcfg = self.env.config.get(u'db', {}) if u'config' in self.env else None
        if not dbcfg:
            raise Exception(u'Невозможно получить параметры соединения с БД')
        host = dbcfg.get(u'host', None)
        database = dbcfg.get(u'database', None)
        user = dbcfg.get(u'user', None)
        password = dbcfg.get(u'password', None)
#        return u"""'Provider=MSDASQL.1;Persist Security Info=False;User ID=%s;Data Source=PostgreSQL35W;Extended Properties="DSN=PostgreSQL35W;DATABASE=%s;SERVER=%s;PORT=5432;UID=%s;SSLmode=disable;ReadOnly=0;Protocol=7.4;FakeOidIndex=0;ShowOidColumn=0;RowVersioning=0;ShowSystemTables=0;ConnSettings=;Fetch=100;Socket=4096;UnknownSizes=0;MaxVarcharSize=255;MaxLongVarcharSize=8190;Debug=0;CommLog=0;Optimizer=0;Ksqo=1;UseDeclareFetch=0;TextAsLongVarchar=1;UnknownsAsLongVarchar=0;BoolsAsChar=1;Parse=0;CancelAsFreeStmt=0;ExtraSysTablePrefixes=dd_;LFConversion=1;UpdatableCursors=1;DisallowPremature=0;TrueIsMinus1=0;BI=0;ByteaAsLongVarBinary=0;UseServerSidePrepare=0;LowerCaseIdentifier=0;GssAuthUseGSS=0;XaOpt=1"'""" % (user, database, host, password) 
        return u"""'Provider=MSDASQL.1;Persist Security Info=False;User ID=%s;Data Source=PostgreSQL35W;Extended Properties="DSN=PostgreSQL35W;DATABASE=%s;SERVER=%s;PORT=5432;UID=%s;password=%s;SSLmode=disable;ReadOnly=0;Protocol=7.4;FakeOidIndex=0;ShowOidColumn=0;RowVersioning=0;ShowSystemTables=0;ConnSettings=;Fetch=100;Socket=4096;UnknownSizes=0;MaxVarcharSize=255;MaxLongVarcharSize=8190;Debug=0;CommLog=0;Optimizer=0;Ksqo=1;UseDeclareFetch=0;TextAsLongVarchar=1;UnknownsAsLongVarchar=0;BoolsAsChar=1;Parse=0;CancelAsFreeStmt=0;ExtraSysTablePrefixes=dd_;LFConversion=1;UpdatableCursors=1;DisallowPremature=0;TrueIsMinus1=0;BI=0;ByteaAsLongVarBinary=0;UseServerSidePrepare=0;LowerCaseIdentifier=0;GssAuthUseGSS=0;XaOpt=1"'""" % (user, database, host, password, password) 

    def set_parameters(self):
        for pname, value in self.params.iteritems():
            self.fr.SetVariable(pname, value)

    def print_(self):
        self.fr.PrintOptions.ShowDialog = False
        self.fr.PrepareReport(True)
        self.fr.PrintReport()

    def preview(self):
        self.fr.ShowReport()

    def design(self):
        self.fr.DesignReport()


class NCPrintForm(BasePrintForm):
    pass

