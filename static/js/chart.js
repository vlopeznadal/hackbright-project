'use strict';
$.get('/ratings', response => {
    (() => {
    const svg = d3.select('#ratings-chart svg');

    const ratings = []
    ratings.push(response['yelp'] * 10);
    ratings.push(response['google'] * 10);
    ratings.push(response['fs']/2 * 10);

    svg
        .selectAll('rect')
        .data(ratings)
        .enter()
        .append('rect')
        .attr('y', (num, idx) => idx * 40)
        .attr('x', 0)
        .attr('width', num => num)
        .attr('height', 30)
        .attr('fill', "steelblue")
        .attr('font', "10px sans-serif")
        .attr('text-align', "right")
        .attr('color', "black")

    svg
        .append("text")
        .attr('text-anchor', 'right')
        .text(ratings[0]);

    })();

});