unit Unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, FileUtil, BCPort, Forms, Controls, Graphics, Dialogs,
  StdCtrls, ExtCtrls, Spin, IniPropStorage, Windows;

type

  { TForm1 }

  TForm1 = class(TForm)
    BComPort1: TBComPort;
    Bevel2: TBevel;
    Bevel3: TBevel;
    Bevel4: TBevel;
    Bevel5: TBevel;
    Button1: TButton;
    Button2: TButton;
    Button3: TButton;
    CheckBox1: TCheckBox;
    CheckBox2: TCheckBox;
    CheckBox3: TCheckBox;
    CheckBox4: TCheckBox;
    CheckBox5: TCheckBox;
    CheckBox6: TCheckBox;
    CheckBox7: TCheckBox;
    CheckBox8: TCheckBox;
    CheckBox9: TCheckBox;
    ComboBox1: TComboBox;
    ComboBox2: TComboBox;
    Edit1: TEdit;
    Edit2: TEdit;
    Edit3: TEdit;
    Edit4: TEdit;
    Edit5: TEdit;
    IniPropStorage1: TIniPropStorage;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    Label7: TLabel;
    Label8: TLabel;
    Label9: TLabel;
    Memo1: TMemo;
    Panel1: TPanel;
    Timer1: TTimer;
    Timer2: TTimer;
    procedure BComPort1RxChar(Sender: TObject; Count: Integer);
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure CheckBox6Change(Sender: TObject);
    procedure ComboBox1DropDown(Sender: TObject);
    procedure ComboBox2DblClick(Sender: TObject);
    procedure ComboBox2DropDown(Sender: TObject);
    procedure Edit1Change(Sender: TObject);
    procedure Edit3Change(Sender: TObject);

    procedure Edit5Change(Sender: TObject);
    procedure FormClose(Sender: TObject; var CloseAction: TCloseAction);
    procedure FormCreate(Sender: TObject);
    procedure Memo1Change(Sender: TObject);
    procedure Timer2Timer(Sender: TObject);
  private
    { private declarations }
  public
    { public declarations }
  end;

var
  Form1: TForm1;
  //Отправленый массив
  SendMas: array[1..1000] of Byte;
  SendKol: Word;
  //Принятый массив
  ReadMas: array[1..2000] of Byte;
  ReadKol: Word;
  //Фильтр
  FiltrMas: array[1..1000] of Byte;
  FiltrKol: Word;
  StartSend: DWORD;
  TimeFiltr: DWORD;
  //строка для отправки в txt документ
  mytxt: TextFile;

implementation

{$R *.lfm}

{ TForm1 }

procedure TForm1.ComboBox1DropDown(Sender: TObject);
begin
   // Список СОМ-портов компьютера
  BComPort1.EnumComPorts(ComboBox1.Items);
end;

procedure TForm1.ComboBox2DblClick(Sender: TObject);
begin

end;

procedure TForm1.ComboBox2DropDown(Sender: TObject);
begin
  // Список СОМ-портов компьютера
 BComPort1.EnumComBaudRate(ComboBox2.Items);
end;
{
function Hex(S: String):DWord;
begin
if (S1[1]<>'#') and (S1[1]<>'$') then
  SendMas[SendKol]:=StrToIntDef(S1,0)
else
  begin
    if Length(S1)>1 then
      begin
        SendMas[SendKol]:=0;
        for x:=2 to Length(S1) do
          begin
            SendMas[SendKol]:=SendMas[SendKol] * 16;
            if (S1[x]>='0') and (S1[x]<='9') then
              SendMas[SendKol]:=SendMas[SendKol]+ord(S1[x])-ord('0')
            else
              if (S1[x]>='A') and (S1[x]<='F') then
                SendMas[SendKol]:=SendMas[SendKol]+ord(S1[x])-ord('A')+10
              else
                if (S1[x]>='a') and (S1[x]<='f') then
                  SendMas[SendKol]:=SendMas[SendKol]+ord(S1[x])-ord('f')+10;

          end;

      end
    else
      SendMas[SendKol]:=0;
  end;
end;
 }
procedure TForm1.Edit1Change(Sender: TObject);
//Создание строки для отправки
// Edit1 Edit2 CheckBox1 CheckBox2
var
  x : byte;
  s, s1: string;
begin
  SendKol:=0;
  if Length(Edit1.Caption) > 0 then
    begin
      for x:=1 to Length(Edit1.Caption) do
        SendMas[x] := ord(Edit1.Caption[x]);
      SendKol:= Length(Edit1.Caption);
    end;
  if Length(Edit2.Caption) > 0 then
    begin
      s:= Edit2.Caption;
      x:= Pos(',',Edit2.Caption);      //поиск ,
      while x>0 do
        begin
          s1:= Copy(s,1,x-1);
          s := Copy(s,x+1,Length(s));
          SendKol:=SendKol+1;
          if Length(S1)>0 then
            if S1[1]='#' then S1[1]:='$';
          SendMas[SendKol]:=StrToIntDef(S1,0);
          x:= Pos(',',S);
        end;
      SendKol:=SendKol+1;
      if Length(S)>0 then
        if S[1]='#' then S[1]:='$';
      SendMas[SendKol]:=StrToIntDef(S,0);
    end;
  if CheckBox1.Checked then
    Begin
      SendKol:=SendKol+1;
      SendMas[SendKol]:=13;
    end;
  if CheckBox2.Checked then
    Begin
      SendKol:=SendKol+1;
      SendMas[SendKol]:=10;
    end;
end;

procedure TForm1.Edit3Change(Sender: TObject);
//Создание строки для отправки
// Edit3 Edit4 CheckBox3 CheckBox42
var
  x : byte;
  s, s1: string;
begin
  FiltrKol:=0;
  if Length(Edit3.Caption) > 0 then
    begin
      for x:=1 to Length(Edit3.Caption) do
        FiltrMas[x] := ord(Edit3.Caption[x]);
      FiltrKol:= Length(Edit3.Caption);
    end;
  if Length(Edit4.Caption) > 0 then
    begin
      s:= Edit4.Caption;
      x:= Pos(',',Edit4.Caption);      //поиск ,
      while x>0 do
        begin
            s1:= Copy(s,1,x-1);
            s := Copy(s,x+1,Length(s));
            FiltrKol:=FiltrKol+1;
          	  if Length(S1)>0 then
                if S1[1]='#' then S1[1]:='$';
            FiltrMas[FiltrKol]:=StrToIntDef(S1,0);
            x:= Pos(',',S);
        end;
      FiltrKol:=FiltrKol+1;
  	  if Length(S1)>0 then
        if S[1]='#' then S[1]:='$';
      FiltrMas[FiltrKol]:=StrToIntDef(S,0);
    end;
  if CheckBox3.Checked then
    Begin
      FiltrKol:=FiltrKol+1;
      FiltrMas[FiltrKol]:=13;
    end;
  if CheckBox4.Checked then
    Begin
      FiltrKol:=FiltrKol+1;
      FiltrMas[FiltrKol]:=10;
    end;

end;

procedure TForm1.Edit5Change(Sender: TObject);
// для CheckBox5 и Edit5
var
  x:integer;
begin
  x:= StrToIntDef(Edit5.Text,0);
  if x=0 then CheckBox5.Checked:=False;
  Timer1.Enabled:=CheckBox5.Checked;
  Timer1.Interval:=x;
end;

procedure TForm1.FormClose(Sender: TObject; var CloseAction: TCloseAction);
begin
    if BComPort1.Connected then // Порт открыт
    begin
      BComPort1.Close;
    end

end;

procedure TForm1.FormCreate(Sender: TObject);
begin
 BComPort1.Port:=ComboBox1.Text;
 BComPort1.BaudRate:= TBaudRate(ComboBox2.ItemIndex);
end;

procedure TForm1.Memo1Change(Sender: TObject);
begin
  SendMessage( Memo1.Handle, EM_LINESCROLL, 0, Memo1.Lines.Count-1 );

end;

procedure TForm1.Timer2Timer(Sender: TObject);
var
  X : DWORD;
begin
  X:= (TimeFiltr	* 1000 )div Timer2.Interval;
  Label9.Caption:='Частота обмена данными: '+ inttostr(X)+ ' Гц';
  if BComPort1.Connected then // Порт открыт
  	memo1.Lines.Add('Частота обмена данными: '+ inttostr(X)+ ' Гц');
  Application.ProcessMessages;
  TimeFiltr:=0;
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
  if BComPort1.Connected then // Порт открыт
    begin
      BComPort1.Close;
    end
  else
    begin
      ReadKol:=0;
      TimeFiltr:=0;
      BComPort1.Port:=ComboBox1.Text;
      if ComboBox2.ItemIndex = -1 then
        begin
		  BComPort1.BaudRate:= TBaudRate(0);
		  BComPort1.CustomBaudRate:=StrToIntDef(ComboBox2.Text,9600);
        end
      else BComPort1.BaudRate:= TBaudRate(ComboBox2.ItemIndex);

      BComPort1.Open;
    end;

  if BComPort1.Connected then // Порт открыт
    begin
      Button1.Caption:='Отключить';
      ComboBox1.Enabled:=False;
      ComboBox2.Enabled:=False;
      Button3.Enabled:=True;
    end
  else
    begin
      Button1.Caption:='Подключить';
      ComboBox1.Enabled:=True;
      ComboBox2.Enabled:=True;
      Button3.Enabled:=False;
    end;
end;

procedure TForm1.BComPort1RxChar(Sender: TObject; Count: Integer);
var
  S: string;
  x: word;
  y: word;
  Mas: array[1..500] of Byte;
  TimeSend: DWORD;
  flag: boolean;
begin
 Count:=BComPort1.Read(Mas,Count);

 TimeSend:=GetTickCount-StartSend;

 if CheckBox8.Checked then
   begin
     s:='';
     for x:=1 to Count do
       if Mas[x]>=30 then
          s:=s+ chr(Mas[x])
       else
          s:=s+ '+#'+inttostr(Mas[x]);

   	 memo1.Lines.Add('Принято:   '+S);
         assignFile(mytxt,'%Temp%\Example.txt');
         rewrite(mytxt);
         writeln(mytxt,S);
         closeFile(mytxt);
   end;

  if CheckBox6.Checked then
    begin
      if FiltrKol>0 then
         begin
           if Count+ReadKol > 2000 then Count:=2000 - ReadKol;

           if Count>0 then
             begin
               for x:= 1 to Count do
                 ReadMas[x+ReadKol]:=Mas[x];
               ReadKol:=ReadKol+Count;

               while FiltrKol<=ReadKol  do
                 begin
                   flag:=True;
                   for x:=1 to FiltrKol do
                     if ReadMas[x]<>FiltrMas[x] then
                       begin
                         flag:=False;
                         break;
                       end;
                   if flag then
                     begin //найдена строка
                       Button3Click(Sender); //Отправка сообщения
                       y:=FiltrKol;

                       Label8.Caption:='Время между пакетами: '+ inttostr(TimeSend)+ ' ms';
                       if CheckBox9.Checked then
                         memo1.Lines.Add('Время между пакетами: '+ inttostr(TimeSend)+ ' ms');
                       TimeFiltr:=TimeFiltr+1;
                     end
                   else
                     begin
                       y:=1;
                     end;
               	   for x:=1 to ReadKol-y do
                    ReadMas[x]:=ReadMas[x+y];
                   ReadKol:=ReadKol-y;

                 end;
             end;
         end;
     end
   else
     begin
       Label8.Caption:='Время между отправкой и приемом: '+ inttostr(TimeSend)+ ' ms';
       if CheckBox9.Checked then
         memo1.Lines.Add('Время между отправкой и приемом: '+ inttostr(TimeSend)+ ' ms');
     end;


end;

procedure TForm1.Button2Click(Sender: TObject);
begin
  Memo1.Clear;
end;

procedure TForm1.Button3Click(Sender: TObject);
//Отправить сообщение
// Button3  Timer1
var
  s:string;
  x: word;
begin
 if SendKol>0 then
   if BComPort1.Connected then // Порт открыт
     begin
       StartSend:=GetTickCount;
       BComPort1.Write(SendMas,SendKol);
       if CheckBox7.Checked then
         begin
           s:='';
           for x:=1 to SendKol do
             if SendMas[x]>=30 then
                s:=s+ chr(SendMas[x])
             else
                s:=s+ '+#'+inttostr(SendMas[x]);
          Memo1.Lines.Add('Отравлено: '+s);
         end;
     end;
end;

procedure TForm1.CheckBox6Change(Sender: TObject);
begin
  Timer2.Enabled:=CheckBox6.Checked;
end;

end.

