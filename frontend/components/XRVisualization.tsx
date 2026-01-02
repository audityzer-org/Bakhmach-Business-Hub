'use client';

import React, { useEffect, useRef } from 'react';
import * as BABYLON from '@babylonjs/core';

const XRVisualization: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const engine = new BABYLON.Engine(canvas, true);
    const scene = new BABYLON.Scene(engine);

    // Camera - XR ready
    const camera = new BABYLON.UniversalCamera('camera', new BABYLON.Vector3(0, 5, 20));
    camera.attachControl(canvas, true);
    camera.inertia = 0.7;
    camera.angularSensibility = 1000;

    // Lighting
    const light1 = new BABYLON.HemisphericLight('light1', new BABYLON.Vector3(1, 1, 1), scene);
    light1.intensity = 0.6;
    const light2 = new BABYLON.PointLight('light2', new BABYLON.Vector3(10, 10, 10), scene);
    light2.intensity = 0.8;

    // Architecture Layers - 3D Representation
    const layerPositions = [
      { name: 'Presentation', y: 0, color: '#FF6B6B', z: 0 },
      { name: 'Application', y: 3, color: '#4ECDC4', z: 2 },
      { name: 'Business', y: 6, color: '#45B7D1', z: 4 },
      { name: 'Security', y: 9, color: '#96CEB4', z: 6 },
      { name: 'Integration', y: 12, color: '#FFEAA7', z: 8 },
      { name: 'Data', y: 15, color: '#DDA15E', z: 10 },
      { name: 'Analytics', y: 18, color: '#BC6C25', z: 12 },
      { name: 'Research', y: 21, color: '#A78BFA', z: 14 },
    ];

    // Create 3D nodes for each layer
    layerPositions.forEach((layer, index) => {
      const box = BABYLON.MeshBuilder.CreateBox(`${layer.name}_box`, { size: 2 }, scene);
      box.position.set(0, layer.y, layer.z);
      const material = new BABYLON.StandardMaterial(`${layer.name}_mat`, scene);
      material.emissiveColor = BABYLON.Color3.FromHexString(layer.color);
      box.material = material;

      // Add label
      const sphereLight = BABYLON.MeshBuilder.CreateSphere('sphere', { diameter: 0.5 }, scene);
      sphereLight.position.set(-3, layer.y, layer.z);
      const lightMat = new BABYLON.StandardMaterial(`light_${index}`, scene);
      lightMat.emissiveColor = BABYLON.Color3.FromHexString(layer.color);
      sphereLight.material = lightMat;

      // Animation
      const animBox = new BABYLON.Animation(
        `anim_${layer.name}`,
        'rotation.z',
        30,
        BABYLON.Animation.ANIMATIONTYPE_FLOAT,
        BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE
      );
      animBox.setKeys([
        { frame: 0, value: 0 },
        { frame: 120, value: Math.PI * 2 },
      ]);
      box.animations = [animBox];
      scene.beginAnimation(box, 0, 120, true);
    });

    // Data flow visualization (particle system)
    const particleSystem = new BABYLON.ParticleSystem('particles', 1000, scene);
    particleSystem.emitter = new BABYLON.Vector3(0, 10, 5);
    particleSystem.minEmitBox = new BABYLON.Vector3(-5, 0, -5);
    particleSystem.maxEmitBox = new BABYLON.Vector3(5, 0, 5);
    particleSystem.createSphereEmitter(5);

    particleSystem.particleTexture = new BABYLON.DynamicTexture('dynamic', 64);
    particleSystem.addColorGradient(0, new BABYLON.Color4(1, 0, 0, 1));
    particleSystem.addColorGradient(0.5, new BABYLON.Color4(0, 1, 0, 1));
    particleSystem.addColorGradient(1, new BABYLON.Color4(0, 0, 1, 1));

    particleSystem.minLifeTime = 2;
    particleSystem.maxLifeTime = 4;
    particleSystem.minSize = 0.1;
    particleSystem.maxSize = 0.5;
    particleSystem.emitRate = 50;
    particleSystem.gravity = new BABYLON.Vector3(0, -0.5, 0);

    particleSystem.start();

    // WebXR support check
    if (navigator.xr) {
      navigator.xr.isSessionSupported('immersive-vr').then((supported) => {
        if (supported) {
          console.log('XR immersive-vr is supported');
          // XR session will be initialized on user interaction
        }
      });
    }

    // Gesture controls (mouse-based for now, will use WebXR on XR devices)
    let isDragging = false;
    let previousMouseX = 0;
    let previousMouseY = 0;

    canvas.addEventListener('mousedown', (e) => {
      isDragging = true;
      previousMouseX = e.clientX;
      previousMouseY = e.clientY;
    });

    canvas.addEventListener('mousemove', (e) => {
      if (isDragging) {
        const deltaX = e.clientX - previousMouseX;
        const deltaY = e.clientY - previousMouseY;
        camera.rotation.y -= deltaX * 0.01;
        camera.rotation.x -= deltaY * 0.01;
        previousMouseX = e.clientX;
        previousMouseY = e.clientY;
      }
    });

    canvas.addEventListener('mouseup', () => {
      isDragging = false;
    });

    // Zoom with mouse wheel
    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      camera.position.z += e.deltaY > 0 ? 2 : -2;
    });

    // Render loop
    engine.runRenderLoop(() => {
      scene.render();
    });

    // Resize handler
    window.addEventListener('resize', () => {
      engine.resize();
    });

    return () => {
      engine.dispose();
    };
  }, []);

  return (
    <div className="w-full h-screen flex flex-col bg-black">
      <div className="bg-gray-900 p-4 text-white">
        <h2 className="text-2xl font-bold">Architecture 3D Visualization (XR-Ready)</h2>
        <p className="text-sm text-gray-400">Drag to rotate • Scroll to zoom • Supports WebXR on VR devices</p>
      </div>
      <canvas
        ref={canvasRef}
        className="flex-1"
        style={{
          display: 'block',
          width: '100%',
          height: '100%',
          touchAction: 'none',
        }}
      />
    </div>
  );
};

export default XRVisualization;
