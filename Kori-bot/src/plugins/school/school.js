const lib = require('lib')({token: process.env.STDLIB_SECRET_TOKEN});


// Write some custom code here


var new_date = new Date(); //新建一个日期对象，默认现在的时间
var date0 = new Date("2021-8-31 22:50:00"); //设置过去的一个时间点，"yyyy-MM-dd HH:mm:ss"格式化日期
var dates = new Date("2021-6-28 16:00:00");
var date1 = new Date("2022-2-4 00:30:00");

var difftime0 = (date0 - new_date); //计算时间差
var difftime = difftime0/1000;

var days = parseInt(difftime/86400); // 天  24*60*60*1000 
var hours = parseInt(difftime/3600)-24*days;    // 小时 60*60 总小时数-过去的小时数=现在的小时数 
var minutes = parseInt(difftime%3600/60); // 分钟 -(day*24) 以60秒为一整份 取余 剩下秒数 秒数/60 就是分钟数
var seconds = parseInt(difftime%60);  // 以60秒为一整份 取余 剩下秒数

// var length = parseInt(Math.log10(date0 - new_date))+1;
// var ms = difftime0%(10**(length-1));
// var total_s = (date0-dates)/1000;

var max=64;

if (new_date<date0){

  var percent=(100-(difftime0/(date0-dates)*100)).toFixed(3);

  var result=("距离开学(*2021-9-1 06:50*)还有 **`"+days+"`天`"+hours+"`小时`"+minutes+"`分钟`"+seconds+"`秒**  (即**`"+(difftime.toLocaleString())+"`秒**) !\n[**");

  //+"["+"█"*(difftime/dates*10)+"░"*(10-(difftime/dates*10))+"]"
  for (let i=0;i<(max-parseInt(difftime0/(date0-dates))*max)+1;i++){
    result += "l";
    // var result=result_;
  }
  for (let i=0;i<((parseInt(difftime0/(date0-dates)*max))+1);i++){
    result+='.';
    // var result=result_;
  }

  result+="**]\n\t\t\t\t\t\t\t";
  result+=(percent+"%");
}else{
  
  difftime*=-1;
  difftime0*=-1;
  days*=-1;
  hours*=-1;
  minutes*=-1;
  seconds*=-1;
  var percent=(100-(difftime0/(date1-date0)*100)).toFixed(3);
  
  var result=("已经开学了 **`"+days+"`天`"+hours+"`小时`"+minutes+"`分钟`"+seconds+"`秒**  (即**`"+(difftime.toLocaleString())+"`秒**) !\n[**");
  
  for (let i=0;i<(25-parseInt(difftime0/(date1-date0))*25)+1;i++){
    result += "#";
    // var result=result_;
  }
  for (let i=0;i<((parseInt(difftime0/(date1-date0)*25))+1);i++){
    result+="   ";
    // var result=result_;
  }
  
   result+="**]";
   result+=(percent+"%");
  
}


await lib.discord.channels['@0.0.6'].messages.create({
  channel_id: context.params.event.channel_id,
  content: `<@!${context.params.event.member.user.id}> just triggered the **school countdown**!\n`+result
});

// await lib.discord.channels['@0.0.6'].messages.create({
//   channel_id: context.params.event.channel_id,
//   content: `\n<:face_with_water:873180466486853642>`
// });





