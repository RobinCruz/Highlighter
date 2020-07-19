from django.shortcuts import render
from django.http import HttpResponse
from . import summarize as sze
from . import summarize_url as surl
import math
# Create your views here.
def home(request):
	if request.method == "POST":
		Para = request.POST.get("Paragraph")
		url = request.POST.get("URL")
		if url != "":
			Para = surl.scrape(url)
		Head = "Summary of the Paragraph"
		Stat = "Statistics"
		Summ = sze.call(Para)
		WordV = len(Para.split())-len(Summ.split())
		PercV = str(math.floor((WordV/len(Para.split()))*100))+"%"
		WordA = "No. of words reduced : "
		PercA = "Percentage reduced   : "
		Of = " Of "
		ParaW = len(Para.split())
		TimeA = "Total Time saved     : "
		TValue = WordV/200
		Hr = math.floor(math.floor(TValue)/60)
		TValue -= Hr*60
		Min = math.floor(TValue)
		TValue -= Min
		Sec = math.floor(TValue*0.60*100)
		TimeV = ""
		if Hr>=1:
			TimeV+=str(Hr)
			if Hr>1:
				TimeV+=" Hours "
			else:
				TimeV+=" Hour "	
		if Min>=1:
			TimeV+=str(Min)
			if Min>1:
				TimeV+=" Minutes "
			else:
				TimeV+=" Minute "
		if Sec>=1:
			TimeV+=str(Sec)
			if Sec>1:
				TimeV+=" Seconds "
			else:
				TimeV+=" Second "						
		
		return render(request, 'P2S/home.html',{"Summ":Summ,"Head":Head,"Para":Para,"WordV":WordV,
			"WordA":WordA,"PercV":PercV,"PercA":PercA,"Stat":Stat,"Of":Of,"ParaW":ParaW,"TimeA":TimeA,
			"TimeV":TimeV})
	else:
		return render(request, 'P2S/home.html')



