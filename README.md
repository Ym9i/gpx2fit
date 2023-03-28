# gpx2fit convert .gpx to .fit
convert gpx 2 fit activity with specified sport type, for Strava upload


## gpx to fit
```sh
pip install -r requirements.txt 
cp .env.example .env
# edit .env file 

python gpx_2_fit.py
```

sport type
- running
- cycling
- hiking
- swimming

## upload to strava 

```sh
pip install -r requirements.txt 
cp .env.example .env
# edit .env file 

python fit_2_strava.py
```

get  `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, `STRAVA_REFRESH_TOKEN`

[ref: running_page#strava](https://github.com/yihong0618/running_page#strava), step 1 ~ 6

---

- https://www.strava.com/settings/api
- https://developers.strava.com/docs/#rate-limiting
```
Strava API Rate Limit Exceeded. Retry after 100 seconds
Strava API Rate Limit Timeout. Retry in 799.491622 seconds
```

## TO DO
- [x] Upload fit to Strava
- [ ] Format Python code

## Thanks
[stagescycling/python_fit_tool](https://bitbucket.org/stagescycling/python_fit_tool/src/main)
