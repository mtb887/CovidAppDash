@@ -0,0 +1,48 @@
+
+#I just need to create a scrub function to pull data directly from a live database. i need more hours in a day.
+
+#This loads the dataset and collects the top 10 regions with the largest number of corona cases
+
+#To anyone who wishes to reuse this code, please remember to install flask, else it wont work. 
+
+def find_top_confirmed(n = 10):
+
+  import pandas as pd
+  corona_df = pd.read_csv('dataset.csv')
+  # i need to change this to make it work with my new data sources, so need to add more columns and aggrigate from there(I really need more hours in a day)
+  by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
+  covid_DF = by_country.nlargest(n, 'Confirmed')[['Confirmed']] #this will return an updated data Frame
+  return covid_DF
+
+
+#make use of  to create a sample map with circles around areas with active corona cases
+import folium
+import pandas as pd
+corona_df = pd.read_csv('recentcovid.csv')
+
+corona_df=corona_df.dropna()
+
+m=folium.Map(location=[34.223334,-82.461707],
+            tiles='Stamen toner',
+            zoom_start=8)
+
+def circle_maker(x):
+    folium.Circle(location=[x[0],x[1]],
+                 radius=float(x[2])*10,
+                 color="red",
+                 popup='{}\n confirmed cases:{}'.format(x[3],x[2])).add_to(m)
+corona_df[['Lat','Long_','Confirmed','Combined_Key']].apply(lambda x:circle_maker(x),axis=1)
+
+html_map=m._repr_html_()#renders map in HTML
+
+#make use of flask to process the data
+from flask import Flask,render_template
+
+app=Flask(__name__)
+
+@app.route('/')
+def home():
+    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)
+
+if __name__=="__main__":
+    app.run(debug=True)
