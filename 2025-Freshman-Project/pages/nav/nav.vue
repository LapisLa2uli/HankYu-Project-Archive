<template>
	<view>

		<view class="imgRow">
			<view v-if="junctionList.length>0">
				<image :src="junctionList[currentJunc].image" class="junctionPic" />
			</view>
			
			<view class="directions">
				<view v-if="junctionList.length>0">
					<view class='junctionName'>{{junctionList[currentJunc].name}}</view>
					<view class='junctionDirections'>{{junctionList[currentJunc].description}}</view>
					<view v-if="currentJunc===junctionList.length-1">
						<button class="finishButton" @click="navigateBack">到达目的地</button>
					</view> 
					<view v-else>
						<button class="finishButton" @click="nextJunction">我已到达</button>
					</view>
				</view>
			</view>
		</view>

		<view class="map-wrap">
			<image src="/static/test2.svg" class="map"></image>
			<canvas canvas-id="routeCanvas" class="route-canvas"></canvas>
		</view>
	</view>
</template>
<script>
	export default {
		onReady() {
			const ctx = uni.createCanvasContext('routeCanvas');
			// 设置 canvas 的宽度和高度
			// 开始绘制路线
			ctx.beginPath();
			// 移动到起始点
			ctx.moveTo(this.routePoints[this.currentMethod][0].x, this.routePoints[this.currentMethod][0].y);
			for (let i = 1; i < this.routePoints[this.currentMethod].length; i++) {
			  // 绘制线段
			  ctx.lineTo(this.routePoints[this.currentMethod][i].x, this.routePoints[this.currentMethod][i].y);
			}
			// 设置路线颜色
			ctx.strokeStyle = ['red','green','blue'][this.currentMethod];
			// 设置路线宽度
			ctx.lineWidth = 2;
			// 设置线段端点样式
			ctx.lineCap = 'round';
			// 设置线段转角样式
			ctx.lineJoin = 'round';
			// 绘制路线
			ctx.stroke();
			// 将绘制内容渲染到 canvas 上
			ctx.draw();
			
		},
		data() {
			return {
				currentMethod: 0,
				junctionList: [],
				currentJunc: 0,
				navigateList: [{
						index: 0,
						x: 0,
						y: 0,
						type: 1, //0-中间点；1-起点；2-终点；3-路口
					},
					{
						index: 1,
						x: 0,
						y: 0,
						type: 0,
					},
					{
						index: 2,
						x: 0,
						y: 0,
						type: 3,
						image: '/static/Pic1.jpg',
						name: '路口1',
						description: '在图中的路口向左转'
					},
					{
						index: 3,
						x: 0,
						y: 0,
						type: 0,
					},
					{
						index: 4,
						x: 0,
						y: 0,
						type: 3,
						image: '/static/Pic2.jpg',
						name: '路口2',
						description: '在图中的路口向右转'
					},
					{
						index: 5,
						x: 0,
						y: 0,
						type: 3,
						image: '/static/Pic3.jpg',
						name: '路口3',
						description: '在图中的路口向左转'
					},
					{
						index: 6,
						x: 0,
						y: 0,
						type: 3,
						image: '/static/Pic4.jpg',
						name: '路口4',
						description: '在图中的路口向右转'
					},
					{
						index: 7,
						x: 0,
						y: 0,
						type: 2,
						image: '',
						name: '终点',
						description: '前方到达终点'
					},
				],
				routePoints:
				[
					[
					        { x: 260, y: 150 },
							{ x: 280, y: 150 },
							{ x: 280, y: 125 },
							{ x: 292, y: 125 },
							{ x: 292, y: 97 },
							{ x: 290, y: 94 },
							{ x: 290, y: 70 },
					        { x: 300, y: 70 },
							
					      ],
					[
					        { x: 260, y: 150 },
							{ x: 280, y: 150 },
							{ x: 280, y: 125 },
							{ x: 262, y: 125 },
							{ x: 262, y: 80 },
							{ x: 290, y: 70 },
					        { x: 300, y: 70 }
					      ],
					[
					        { x: 260, y: 150 },
							{ x: 280, y: 150 },
							{ x: 280, y: 125 },
							{ x: 310, y: 125 },
							{ x: 310, y: 97 },
							{ x: 312, y: 94 },
							{ x: 312, y: 70 },
					        { x: 300, y: 70 },
							
					      ],
				],
				
				// 固定的宽度和高度
				fixedWidth: 400,
				fixedHeight: 300,
				mapImageUrl: '@/static/map1.svg'
			}
		},
		onLoad(options) {
			this.currentMethod=options.index  
			this.junctionList = this.navigateList.filter((i) => {
				return i.type === 3 || i.type === 2
			})
			console.log(this.junctionList[0].image)
		},
		methods: {
			nextJunction() {
				this.currentJunc += 1

			},
			navigateBack() {
				uni.reLaunch({
					url: "/pages/index/index"
				})
			}
		}
	}
</script>
<style>
	.imgRow {
		display: flex;
		flex-direction: row;
	}

	.junctionPic {
		width: 200rpx;
		height: 200rpx;
		margin: 30rpx;
	}

	.directions {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.junctionName {
		font-size: 50rpx;
		font-weight: bold;
		margin-left: 30rpx;
	}

	.junctionDirections {
		font-size: 40rpx;
		margin: 30rpx;
	}

	.finishButton {
		float: right;
		width: 220rpx;
		margin: 40rpx;
		font-size:24rpx;
		
	}
	.map {
		width: 100%;
	}
	.route-canvas {
	  position: absolute;
	  top: 0;
	  left: 0;
	  width: 400px;
	  height: 300px;
	}
	.map-wrap{
		position: relative;
	}
</style>