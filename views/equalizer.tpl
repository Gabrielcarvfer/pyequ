 <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.2.1.min.js"></script>
<script>
 setInterval(
  function() {
      $.getJSON( "http://localhost:8080/samples", function( data ) {
          var items = data["samples"];
          for (var item in items){
            document.getElementById('equ_bar'+item).setAttribute("height",items[item]+"px")
           };

      });
  }, 100);

</script>

<script>
 document.getElementById("playAudio").addEventListener("click", function(){
      if(this.className == 'is-playing'){
        this.className = "";
        this.innerHTML = "Play"
        //audio.pause();
      }else{
        this.className = "is-playing";
        this.innerHTML = "Pause";
        //audio.play();
      }
    });
</script

<!--animate attributeName="height" calcMode="spline" values="1" times="0;0.33;0.66;1" ng-attr-dur="{{config_speed}}" keySplines="0.5 0 0.5 1;0.5 0 0.5 1;0.5 0 0.5 1" repeatCount="indefinite" begin="-0.5833333333333334s" dur="1">
</animate-->
    <div class="lds-svg ng-scope">
        <svg class="lds-equalizer" width="100%" height="350px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" style="background: rgb(255, 255, 255) none repeat scroll 0% 0%;">
            <g transform="rotate(180 50 50)">
                <rect id="equ_bar0" ng-attr-x="{{7.6923076923076925 - config_width/2}}" y="15" ng-attr-width="{{config_width}}" height="1" fill="#030303" x="2.6923076923076925" width="10">
                </rect>
                <rect id="equ_bar1" ng-attr-x="{{15.384615384615385 - config_width/2}}" y="15" ng-attr-width="{{config_width}}" height="1" fill="#d39182" x="10.384615384615385" width="10">
                </rect>
                <rect id="equ_bar2" ng-attr-x="{{23.076923076923077 - config_width/2}}" y="15" ng-attr-width="{{config_width}}" height="1" fill="#e0e0d0" x="18.076923076923077" width="10">
                </rect>
                <rect id="equ_bar3" ng-attr-x="{{30.76923076923077 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#b4b524" x="25.76923076923077" width="10">
                </rect>
                <rect id="equ_bar4" ng-attr-x="{{38.46153846153846 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#14843c" x="33.46153846153846" width="10">
                </rect>
                <rect id="equ_bar5" ng-attr-x="{{46.15384615384615 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#7c9ba0" x="41.15384615384615" width="10">
                </rect>
                <rect id="equ_bar6" ng-attr-x="{{53.84615384615385 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#1087b0" x="48.84615384615385" width="10">
                </rect>
                <rect id="equ_bar7" ng-attr-x="{{61.53846153846154 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#35578f" x="56.53846153846154" width="10">
                </rect>
                <rect id="equ_bar8" ng-attr-x="{{69.23076923076923 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#2e385b" x="64.23076923076923" width="10">
                </rect>
                <rect id="equ_bar9" ng-attr-x="{{76.92307692307692 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#22202c" x="71.92307692307692" width="10">
                </rect>
                <rect id="equ_bar10" ng-attr-x="{{84.61538461538461 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"  height="1" fill="#6a5363" x="79.61538461538461" width="10">
                </rect>
                <rect id="equ_bar11" ng-attr-x="{{92.3076923076923 - config_width/2}}" y="15" ng-attr-width="{{config_width}}"   height="1" fill="#af243d" x="87.3076923076923" width="10">
                </rect>
            </g>
        </svg>
    </div>
    <form action="play" method="POST" >
        <select name="music" required>
            <option value="0">aha          </option>
            <option value="1">america      </option>
            <option value="2">chilly       </option>
            <option value="3">chilly_sample</option>
            <option value="4">cutcopy      </option>
            <option value="5">duran        </option>
            <option value="6">lambert      </option>
            <option value="7">newell       </option>
        </select>
        <input type="submit" value="Submit">
    </div>

