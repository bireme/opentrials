var scrollInt
var scrTime, scrSt, scrDist, scrDur, scrInt, scrSl, scrDistX

function easeInOut(t,b,c,d)
{
	return (c/2 * (1 - Math.cos(Math.PI*t/d)) + b);
}

scrollPage = function()
{
	scrTime += scrInt

	if (scrTime < scrDur) {
		window.scrollTo(easeInOut(scrTime,scrSl,scrDistX,scrDur), easeInOut(scrTime,scrSt,scrDist,scrDur))
	} else {
		window.scrollTo(scrSl+scrDistX, scrSt+scrDist)
		clearInterval(scrollInt)
	}
}

jQuery.fn.extend({
	smoothScroll : function(duration, velocity, marginLeft, marginTop)
	{
		if(typeof(duration) == 'undefined') duration = 500
		if(typeof(velocity) == 'undefined') velocity = 10
		if(typeof(marginLeft) == 'undefined') marginLeft = 0
		if(typeof(marginTop) == 'undefined') marginTop = 0

		this.click(function(){
			var element_id = $(this).attr("href")
			var source_positions = {
				top : $(this).get(0).offsetTop,
				left : $(this).get(0).offsetLeft
			}
			var dest_positions = {
				top : $(element_id).get(0).offsetTop-marginTop,
				left : $(element_id).get(0).offsetLeft-marginLeft
			}

			if (window.scrollY)
				scrSt = window.scrollY
			else if (document.documentElement.scrollTop)
				scrSt = document.documentElement.scrollTop
			else
				scrSt = document.body.scrollTop
				
			if (window.scrollX)
				scrSl = window.scrollX
			else if (document.documentElement.scrollLeft)
				scrSl = document.documentElement.scrollLeft
			else
				scrSl = document.body.scrollLeft

			scrDist = dest_positions.top - scrSt
			scrDistX = dest_positions.left - scrSl
			scrDur = 500
			scrTime = 0
			scrInt = 5

			// set interval
			clearInterval(scrollInt)
			scrollInt = setInterval(scrollPage, scrInt)

			return false
		})
	}
})