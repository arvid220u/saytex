(* ::Package:: *)

stringIntoTex[string_,debug_:False]:=Module[
	{result,latex},
	result=Interpreter["HeldMathExpression"][string];
	latex=If[
	Not@FailureQ@result,
	StringTake[ToString[ToExpression["TeXForm"][result]], {20, StringLength[ToString[ToExpression["TeXForm"][result]]]}],
	ToString[ToExpression["TeXForm"][ToExpression[ImportString[URLExecute["http://api.wolframalpha.com/v2/query?appid=3TV469-GQUVTHUU6R&format=minput&output=json&input="<>URLEncode[string]], "RawJSON"]["queryresult"]["pods"][[1]]["subpods"][[1]]["minput"],StandardForm,HoldForm]]]
	];
 latex=If[
	Not@FailureQ@result,
 If[StringMatchQ[latex, StartOfString ~~ "\\left[" ~~ __],
 StringTake[latex, {7,StringLength[latex]-7}], StringTake[latex, {2,StringLength[latex]-1}]]
 ,
	latex
	];
	If[debug,{result,latex},latex]
	]
CloudDeploy[APIFunction[{"x"->"String"},stringIntoTex@#x&],"latexdictation/stringtolatex",Permissions->"Public"]
