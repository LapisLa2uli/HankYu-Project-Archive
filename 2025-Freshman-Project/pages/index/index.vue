<template>
	<view>
		<block v-if="!isNavigating">
			<view class="content-wrap">
				<view class="content">
					<view class="label">起点</view>
					<view> 
						<picker mode="multiSelector" :range="multiArray" :value="multiIndex" @change="multiPickerChange"
							@columnchange="multiPickerColumnChange">
							<view class="picker">
								{{ multiArray[0][multiIndex[0]] }} - {{ multiArray[1][multiIndex[1]] }}
							</view>
						</picker>
					</view>
					<!-- <input class="input" placeholder="请输入起点" v-model="startLocation" /> -->
				</view> 
				<view class="content">
					<view class="label">终点</view>
					<view>
						<picker mode="multiSelector" :range="multiArray2" :value="multiIndex2" @change="multiPickerChange2"
							@columnchange="multiPickerColumnChange2">
							<view class="picker">
								{{ multiArray2[0][multiIndex2[0]] }} - {{ multiArray2[1][multiIndex2[1]] }}
							</view>
						</picker>
					</view>
				</view>
				<button type="primary" class="button" @click="startNavigate">规划路线</button>
			</view>
		</block>
		<block v-else>
			<view class="navigate-wrap">
				<view class="title-wrap">
					<view class="title">路线规划方案</view>
					<view class="title-item-wrap">
						<view class="title-wrap">
							<image src="/static/qidian.png" class="location-icon" />
							<view>{{startLocation}}</view>
						</view>
						<view class="title-wrap">
							<image src="/static/zhongdian.png" class="location-icon" />
							<view>{{endLocation}}</view>
						</view>
					</view>
				</view>
				<view class="navigate-method-wrap">
					<view :class="currentMethod === 0 ? 'navigate-method-selected' : 'navigate-method'"
						@click="()=>chooseMethod(0)">最近路线</view>
					<view :class="currentMethod === 1 ? 'navigate-method-selected' : 'navigate-method'"
						@click="()=>chooseMethod(1)">最美路线</view>
					<view :class="currentMethod === 2 ? 'navigate-method-selected' : 'navigate-method'"
						@click="()=>chooseMethod(2)">经过地标最多</view>
				</view>
				<button type="primary" class="button" @click="startGuide">开始导航</button>
				<button class="button" @click="cancelNavigate">返回</button>
			</view>
		</block>
		<view class="map-wrap">
			<image src="/static/test2.svg" class="map"></image>
			<canvas canvas-id="routeCanvas" class="route-canvas"></canvas>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				isNavigating: false,
				startLocation: '中兴楼-大门',
				endLocation: '中兴楼-大门',
				currentMethod: 0,
				// 定义每一列的原始数据
				originalArray: [{
						name: '中兴楼',
						children: ['大门', '正门', '小门']
					},
					{
						name: '甄陶楼',
						children: ['南门', '北门']
					},
					{
						name: '龙门楼',
						children: ['南门', '北门','西门']
					},
					{
						name: '大礼堂',
						children: ['北正门', '南正门','西侧门1','西侧门2']
					},
					{
						name: '总务楼',
						children: ['正门', '南侧门','北侧门']
					},
					{
						name: '先棉堂',
						children: ['北门1', '北门2','正门']
					},
					{
						name: '逸夫楼',
						children: ['正门', '南出口','北出口']
					},
					{
						name: '西楼A',
						children: ['正门', '南门','北门']
					},
					{
						name: '西楼B',
						children:  ['正门', '南门','北门']
					}, 
					{
						name: '西楼C',
						children:  ['正门', '南门','北门']
					},
					{
						name: '西楼D',
						children:  ['正门', '南门','北门']
					},
					{
						name: '西楼E',
						children:  ['正门', '南门','北门']
					}
				],
				// 多列选择的数据
				multiArray: [
					['中兴楼', '甄陶楼', '龙门楼','大礼堂','总务楼','先棉堂','逸夫楼','西楼A','西楼B','西楼C','西楼D','西楼E'],
					['大门', '正门', '小门']
				],
				// 当前选中的每一列的索引
				multiIndex: [0, 0],
				multiArray2: [
					['中兴楼', '甄陶楼', '龙门楼','大礼堂','总务楼','先棉堂','逸夫楼','西楼A','西楼B','西楼C','西楼D','西楼E'],
					['大门', '正门', '小门']
				],
				// 当前选中的每一列的索引
				multiIndex2: [0, 0],
				routePoints: [
					[{
							x: 260,
							y: 150
						},
						{
							x: 280,
							y: 150
						},
						{
							x: 280,
							y: 125
						},
						{
							x: 292,
							y: 125
						},
						{
							x: 292,
							y: 97
						},
						{
							x: 290,
							y: 94
						},
						{
							x: 290,
							y: 70
						},
						{
							x: 300,
							y: 70
						},

					],
					[{
							x: 260,
							y: 150
						},
						{
							x: 280,
							y: 150
						},
						{
							x: 280,
							y: 125
						},
						{
							x: 262,
							y: 125
						},
						{
							x: 262,
							y: 80
						},
						{
							x: 290,
							y: 70
						},
						{
							x: 300,
							y: 70
						}
					],
					[{
							x: 260,
							y: 150
						},
						{
							x: 280,
							y: 150
						},
						{
							x: 280,
							y: 125
						},
						{
							x: 310,
							y: 125
						},
						{
							x: 310,
							y: 97
						},
						{
							x: 312,
							y: 94
						},
						{
							x: 312,
							y: 70
						},
						{
							x: 300,
							y: 70
						},

					],
				]
			}
		},
		onLoad() {

		},
		methods: {
			startNavigate() {
				this.isNavigating = true
				this.drawRoute(this.routePoints[0])
			},
			cancelNavigate() {
				this.isNavigating = false
				this.clearCanvas()
			},
			chooseMethod(index) {
				this.currentMethod = index
				this.clearCanvas()
				this.drawRoute(this.routePoints[this.currentMethod])
			},
			bindPickerChange: function(e) {
				console.log('picker发送选择改变，携带值为', e.detail.value)
				this.index = e.detail.value
			},
			startGuide() {
				uni.navigateTo({
					url: `/pages/nav/nav?index=${this.currentMethod}`
				})
			},
			// 处理多列选择改变事件
			multiPickerChange(e) {
				console.log('picker 多列选择改变，携带值为', e.detail.value);
				// 更新选中的索引
				this.multiIndex = e.detail.value;
			},
			// 处理列改变事件
			multiPickerColumnChange(e) {
				console.log('列改变，携带值为', e.detail);
				const column = e.detail.column;
				const value = e.detail.value;
				if (column === 0) {
					// 如果第一列发生改变
					// 根据第一列选中的值更新第二列的数据
					this.multiArray[1] = this.originalArray[value].children;
					// 重置第二列的选中索引为 0 
					this.multiIndex[1] = 0;
				}
				// 正确更新当前列的选中索引
				this.multiIndex[column] = value;
				this.startLocation= `${this.multiArray[0][this.multiIndex[0]]} - ${this.multiArray[1][this.multiIndex[1]]}`
				this.$forceUpdate()
			},
			multiPickerChange2(e) {
				console.log('picker 多列选择改变，携带值为', e.detail.value);
				// 更新选中的索引
				this.multiIndex2 = e.detail.value;
			},
			// 处理列改变事件
			multiPickerColumnChange2(e) {
				console.log('列改变，携带值为', e.detail);
				const column = e.detail.column;
				const value = e.detail.value;
				if (column === 0) {
					// 如果第一列发生改变
					// 根据第一列选中的值更新第二列的数据
					this.multiArray2[1] = this.originalArray[value].children;
					// 重置第二列的选中索引为 0
					this.multiIndex2[1] = 0;
				}
				// 正确更新当前列的选中索引
				this.multiIndex2[column] = value;
				this.endLocation= `${this.multiArray2[0][this.multiIndex2[0]]} - ${this.multiArray2[1][this.multiIndex2[1]]}`
				this.$forceUpdate()
			},
			drawRoute(points) {
				const ctx = uni.createCanvasContext('routeCanvas');
				// 设置 canvas 的宽度和高度
				// 开始绘制路线
				ctx.beginPath();
				// 移动到起始点
				ctx.moveTo(points[0].x, points[0].y);
				for (let i = 1; i < points.length; i++) {
					// 绘制线段
					ctx.lineTo(points[i].x, points[i].y);
				}
				// 设置路线颜色
				ctx.strokeStyle = ['red', 'green', 'blue'][this.currentMethod];
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
			clearCanvas() {
				const ctx = uni.createCanvasContext('routeCanvas');
				ctx.clearRect(0, 0, 400, 300);
				ctx.draw()
			}
		}
	}
</script>

<style>
	.content-wrap {
		height: 300rpx;
		padding: 20rpx;
	}

	.content {
		display: flex;
		flex-direction: row;
		align-items: center;
		margin-bottom: 20rpx;
	}

	.content-right {
		display: flex;
		flex-direction: row-reverse;
		justify-content: flex-end;
		align-items: right;
		text-align: right;
	}

	.button {
		width: 160rpx;
		font-size: 24rpx;
		float: right;
		margin: 20rpx;
	}

	.map {
		width: 100%;
	}

	.label {
		margin-right: 20rpx;
	}

	.input {
		border: 1rpx solid #999999;
		padding: 5rpx 10rpx;
	}

	.navigate-wrap {
		padding: 20rpx;
		height: 300rpx;
	}

	.title {
		font-size: 38rpx;
		font-weight: bold;
	}

	.title-wrap {
		display: flex;
		justify-content: space-between;
		margin-bottom: 10rpx;
	}

	.title-item-wrap {
		display: flex;
		flex-direction: column;
	}

	.location-icon {
		width: 60rpx;
		height: 60rpx;
	}

	.navigate-method-wrap {
		display: flex;
		justify-content: space-between;
	}

	.navigate-method {
		padding: 10rpx;
		border: 1px solid #eee;
		border-radius: 10rpx;
	}

	.navigate-method-selected {
		padding: 10rpx;
		border: 1px solid #eee;
		border-radius: 10rpx;
		background-color: #76aa30;
		color: white;
	}

	.map-wrap {
		position: relative;
	}

	.route-canvas {
		position: absolute;
		top: 0;
		left: 0;
		width: 400px;
		height: 300px;
	}
</style>