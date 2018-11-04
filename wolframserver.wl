(* ::Package:: *)

stringIntoTex[string_,debug_:False]:=Module[
{result,latex},
result=Interpreter["HeldMathExpression"][string];
latex=If[
Not@FailureQ@result,
StringReplace[StringTrim@ExportString[result,"TeXFragment"],
{"\\text{HoldComplete}"->"","\\left["->"","\\right]"->""}]
,
ToString[ToExpression["TeXForm"][ToExpression[ImportString[URLExecute["http://api.wolframalpha.com/v2/query?appid=SECRET-API-KEY&format=minput&output=json&input="<>URLEncode[string]], "RawJSON"]["queryresult"]["pods"][[1]]["subpods"][[1]]["minput"],StandardForm,HoldForm]]]
];
If[debug,{result,latex},latex]
]

CloudDeploy[APIFunction[{"x"->"String"},stringIntoTex@#x&],"latexdictation/stringtolatex",Permissions->"Public"]
