%https://stackoverflow.com/questions/31860631/how-to-find-an-arbitrary-perpendicular-vector-of-another-vector-in-matlab

function xout = orthoVector(x, y, z)
    xin = [x;y;z];
    e = xin;
    while ((e'*xin)==xin'*xin)
        e = 2.*rand(3,1)-1;
    end
    xout = cross(xin, e);
    xout = 1.0/(rand()) * xout;
end