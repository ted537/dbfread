from pytest import raises
from dbfread import DBF
from dbfread import MissingMemoFile

def test_missing_memofile():
    with raises(MissingMemoFile):
        DBF('tests/cases/no_memofile.dbf')

    # This should succeed.
    table = DBF('tests/cases/no_memofile.dbf', ignore_missing_memofile=True)

    # Memo fields should be returned as None.
    record = next(iter(table))
    assert record['MEMO'] is None

def test_scx_file():
    ''' Parse an SCX file. Depends on blocksize being read properly. '''
    dbf = DBF(
        'tests/cases/form1.scx', 
        memofilename='tests/cases/form1.SCT',
        load=True
    )
    assert dbf.records[0]['PLATFORM'] == 'COMMENT'
    assert dbf.records[0]['UNIQUEID'] == 'Screen'

    assert dbf.records[1]['OBJNAME'] == 'Dataenvironment'
    assert dbf.records[1]['PROPERTIES'] == (
        'Top = 0\r\nLeft = 0\r\nWidth = 0\r\nHeight = 0\r\n'
        'DataSource = .NULL.\r\nName = "Dataenvironment"\r\n'
    )
    
    assert dbf.records[4]['METHODS'] == (
        'PROCEDURE Init\r\nbtncount = 4\r\n\r\n'
        '*THISFORM.Label1.Caption = STR(btncount)\r\n'
        'ENDPROC\r\n'
        'PROCEDURE Click\r\nTHISFORM.btncount = THISFORM.btncount+1\r\n'
        'THISFORM.label1.Caption = STR(THISFORM.BTNCOUNT)\r\nENDPROC\r\n'
    )